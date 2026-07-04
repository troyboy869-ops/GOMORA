import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

# Serve frontend build if available
static_folder = os.path.join(os.path.dirname(__file__), '../frontend/dist')
if os.path.exists(static_folder):
    app = Flask(__name__, static_folder=static_folder, static_url_path='')
else:
    app = Flask(__name__)

CORS(app)

# ==================== CONFIGURATION ====================

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'postgresql://user:password@localhost:5432/gomora_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key_here')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    playlists = db.relationship('Playlist', backref='user', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Music(db.Model):
    __tablename__ = 'music'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    album = db.Column(db.String(200))
    genre = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    file_path = db.Column(db.String(500), nullable=False)
    cover_art = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    playlists = db.relationship('PlaylistMusic', backref='music', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='music', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'genre': self.genre,
            'duration': self.duration,
            'cover_art': self.cover_art,
            'created_at': self.created_at.isoformat()
        }


class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    musics = db.relationship('PlaylistMusic', backref='playlist', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'music_count': len(self.musics),
            'created_at': self.created_at.isoformat()
        }


class PlaylistMusic(db.Model):
    __tablename__ = 'playlist_music'
    
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.now())


class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'GOMORA API is running'}), 200


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


# ==================== MUSIC ROUTES ====================

@app.route('/api/music', methods=['GET'])
def get_all_music():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    musics = Music.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'musics': [music.to_dict() for music in musics.items],
        'total': musics.total,
        'pages': musics.pages,
        'current_page': page
    }), 200


@app.route('/api/music/<int:music_id>', methods=['GET'])
def get_music(music_id):
    music = Music.query.get(music_id)
    
    if not music:
        return jsonify({'error': 'Music not found'}), 404
    
    return jsonify(music.to_dict()), 200


@app.route('/api/music/search', methods=['GET'])
def search_music():
    query = request.args.get('q', '', type=str)
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    musics = Music.query.filter(
        (Music.title.ilike(f'%{query}%')) |
        (Music.artist.ilike(f'%{query}%')) |
        (Music.album.ilike(f'%{query}%'))
    ).all()
    
    return jsonify({
        'results': [music.to_dict() for music in musics],
        'count': len(musics)
    }), 200


@app.route('/api/music', methods=['POST'])
@jwt_required()
def add_music():
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('artist') or not data.get('file_path'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    music = Music(
        title=data['title'],
        artist=data['artist'],
        album=data.get('album'),
        genre=data.get('genre'),
        duration=data.get('duration'),
        file_path=data['file_path'],
        cover_art=data.get('cover_art')
    )
    
    db.session.add(music)
    db.session.commit()
    
    return jsonify({
        'message': 'Music added successfully',
        'music': music.to_dict()
    }), 201


# ==================== PLAYLIST ROUTES ====================

@app.route('/api/playlists', methods=['GET'])
@jwt_required()
def get_user_playlists():
    user_id = get_jwt_identity()
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'playlists': [playlist.to_dict() for playlist in playlists]
    }), 200


@app.route('/api/playlists', methods=['POST'])
@jwt_required()
def create_playlist():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Playlist name required'}), 400
    
    playlist = Playlist(
        name=data['name'],
        description=data.get('description'),
        user_id=user_id
    )
    
    db.session.add(playlist)
    db.session.commit()
    
    return jsonify({
        'message': 'Playlist created successfully',
        'playlist': playlist.to_dict()
    }), 201


@app.route('/api/playlists/<int:playlist_id>/music', methods=['GET'])
@jwt_required()
def get_playlist_music(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    
    user_id = get_jwt_identity()
    if playlist.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    musics = [pm.music.to_dict() for pm in playlist.musics]
    
    return jsonify({
        'playlist': playlist.to_dict(),
        'musics': musics
    }), 200


@app.route('/api/playlists/<int:playlist_id>/music/<int:music_id>', methods=['POST'])
@jwt_required()
def add_music_to_playlist(playlist_id, music_id):
    user_id = get_jwt_identity()
    playlist = Playlist.query.get(playlist_id)
    music = Music.query.get(music_id)
    
    if not playlist or not music:
        return jsonify({'error': 'Playlist or music not found'}), 404
    
    if playlist.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    existing = PlaylistMusic.query.filter_by(
        playlist_id=playlist_id,
        music_id=music_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Music already in playlist'}), 409
    
    pm = PlaylistMusic(playlist_id=playlist_id, music_id=music_id)
    db.session.add(pm)
    db.session.commit()
    
    return jsonify({'message': 'Music added to playlist'}), 201


@app.route('/api/playlists/<int:playlist_id>/music/<int:music_id>', methods=['DELETE'])
@jwt_required()
def remove_music_from_playlist(playlist_id, music_id):
    user_id = get_jwt_identity()
    playlist = Playlist.query.get(playlist_id)
    
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    
    if playlist.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    pm = PlaylistMusic.query.filter_by(
        playlist_id=playlist_id,
        music_id=music_id
    ).first()
    
    if not pm:
        return jsonify({'error': 'Music not in playlist'}), 404
    
    db.session.delete(pm)
    db.session.commit()
    
    return jsonify({'message': 'Music removed from playlist'}), 200


# ==================== FAVORITES ROUTES ====================

@app.route('/api/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    musics = [fav.music.to_dict() for fav in favorites]
    
    return jsonify({
        'favorites': musics,
        'count': len(musics)
    }), 200


@app.route('/api/favorites/<int:music_id>', methods=['POST'])
@jwt_required()
def add_favorite(music_id):
    user_id = get_jwt_identity()
    music = Music.query.get(music_id)
    
    if not music:
        return jsonify({'error': 'Music not found'}), 404
    
    existing = Favorite.query.filter_by(
        user_id=user_id,
        music_id=music_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Already favorited'}), 409
    
    favorite = Favorite(user_id=user_id, music_id=music_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Music added to favorites'}), 201


@app.route('/api/favorites/<int:music_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(music_id):
    user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(
        user_id=user_id,
        music_id=music_id
    ).first()
    
    if not favorite:
        return jsonify({'error': 'Music not in favorites'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Music removed from favorites'}), 200


# ==================== FRONTEND ROUTES ====================

@app.route('/')
def serve_frontend():
    """Serve the frontend index.html"""
    if os.path.exists(static_folder):
        return send_from_directory(static_folder, 'index.html')
    return jsonify({'message': 'GOMORA API - Frontend not built yet'}), 200


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files or fallback to index.html for SPA routing"""
    if os.path.exists(static_folder):
        file_path = os.path.join(static_folder, path)
        if os.path.exists(file_path):
            return send_from_directory(static_folder, path)
        # Fallback to index.html for SPA routing
        return send_from_directory(static_folder, 'index.html')
    return jsonify({'error': 'Resource not found'}), 404


# ==================== ERROR HANDLERS ====================

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=int(os.getenv('PORT', 5000)))