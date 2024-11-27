from flask import jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Infrastructure
from proxmox_api import ProxmoxAPI

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Vérification si l'utilisateur existe déjà
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Création du nouvel utilisateur
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({
            'message': 'Logged in successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/infrastructure', methods=['POST'])
@login_required
def create_infrastructure():
    data = request.get_json()
    try:
        proxmox = ProxmoxAPI()
        vm_id = proxmox.create_vm(
            name=data['name'],
            cpu_cores=data['cpu_cores'],
            memory=data['memory'],
            disk_size=data['disk_size']
        )
        
        infra = Infrastructure(
            name=data['name'],
            vm_id=vm_id,
            cpu_cores=data['cpu_cores'],
            memory=data['memory'],
            disk_size=data['disk_size'],
            user_id=current_user.id
        )
        
        db.session.add(infra)
        db.session.commit()
        
        return jsonify({
            'message': 'Infrastructure created successfully',
            'infrastructure': {
                'id': infra.id,
                'name': infra.name,
                'vm_id': infra.vm_id,
                'status': infra.status
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/infrastructure', methods=['GET'])
@login_required
def get_infrastructures():
    infrastructures = Infrastructure.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'vm_id': i.vm_id,
        'cpu_cores': i.cpu_cores,
        'memory': i.memory,
        'disk_size': i.disk_size,
        'status': i.status,
        'created_at': i.created_at.isoformat()
    } for i in infrastructures])

@app.route('/api/infrastructure/<int:infra_id>', methods=['GET'])
@login_required
def get_infrastructure(infra_id):
    infra = Infrastructure.query.get_or_404(infra_id)
    if infra.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    return jsonify({
        'id': infra.id,
        'name': infra.name,
        'vm_id': infra.vm_id,
        'cpu_cores': infra.cpu_cores,
        'memory': infra.memory,
        'disk_size': infra.disk_size,
        'status': infra.status,
        'created_at': infra.created_at.isoformat()
    })
