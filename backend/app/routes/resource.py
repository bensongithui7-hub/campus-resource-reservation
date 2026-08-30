from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from app import db
from app.models import Resource


resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/resources", methods=["GET"])
def get_resources():
    resources = Resource.query.all()

    return jsonify({
        "success": True,
        "resources": [
            {
                "id": resource.id,
                "name": resource.name,
                "type": resource.type,
                "description": resource.description,
                "location": resource.location,
                "capacity": resource.capacity,
                "status": resource.status,
                "created_at": resource.created_at.isoformat()
                if resource.created_at else None
            }
            for resource in resources
        ]
    }), 200


@resource_bp.route("/resources/<int:resource_id>", methods=["GET"])
def get_resource(resource_id):
    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    return jsonify({
        "success": True,
        "resource": {
            "id": resource.id,
            "name": resource.name,
            "type": resource.type,
            "description": resource.description,
            "location": resource.location,
            "capacity": resource.capacity,
            "status": resource.status,
            "created_at": resource.created_at.isoformat()
            if resource.created_at else None
        }
    }), 200


@resource_bp.route("/resources", methods=["POST"])
def create_resource():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    resource_type = data.get("type")
    description = data.get("description")
    location = data.get("location")
    capacity = data.get("capacity")

    if not name or not resource_type or not location or capacity is None:
        return jsonify({
            "success": False,
            "message": "Name, type, location and capacity are required"
        }), 400

    if resource_type not in ["LABORATORY", "STUDY_ROOM", "EQUIPMENT"]:
        return jsonify({
            "success": False,
            "message": "Invalid resource type"
        }), 400

    if not isinstance(capacity, int) or capacity < 1:
        return jsonify({
            "success": False,
            "message": "Capacity must be a positive integer"
        }), 400

    resource = Resource(
        name=name,
        type=resource_type,
        description=description,
        location=location,
        capacity=capacity,
        status="AVAILABLE"
    )

    db.session.add(resource)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Resource created successfully",
        "resource": {
            "id": resource.id,
            "name": resource.name,
            "type": resource.type,
            "description": resource.description,
            "location": resource.location,
            "capacity": resource.capacity,
            "status": resource.status,
            "created_at": resource.created_at.isoformat()
            if resource.created_at else None
        }
    }), 201


@resource_bp.route("/admin/resources/<int:resource_id>", methods=["PUT"])
@jwt_required()
def update_resource(resource_id):
    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "name" in data:
        resource.name = data["name"]

    if "type" in data:
        if data["type"] not in [
            "LABORATORY",
            "STUDY_ROOM",
            "EQUIPMENT"
        ]:
            return jsonify({
                "success": False,
                "message": "Invalid resource type"
            }), 400

        resource.type = data["type"]

    if "description" in data:
        resource.description = data["description"]

    if "location" in data:
        resource.location = data["location"]

    if "capacity" in data:
        if not isinstance(data["capacity"], int) or data["capacity"] < 1:
            return jsonify({
                "success": False,
                "message": "Capacity must be a positive integer"
            }), 400

        resource.capacity = data["capacity"]

    if "status" in data:
        if data["status"] not in [
            "AVAILABLE",
            "UNAVAILABLE"
        ]:
            return jsonify({
                "success": False,
                "message": "Invalid resource status"
            }), 400

        resource.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Resource updated successfully",
        "resource": {
            "id": resource.id,
            "name": resource.name,
            "type": resource.type,
            "description": resource.description,
            "location": resource.location,
            "capacity": resource.capacity,
            "status": resource.status,
            "created_at": resource.created_at.isoformat()
            if resource.created_at else None
        }
    }), 200


@resource_bp.route("/admin/resources/<int:resource_id>", methods=["DELETE"])
@jwt_required()
def delete_resource(resource_id):
    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    db.session.delete(resource)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Resource deleted successfully"
    }), 200