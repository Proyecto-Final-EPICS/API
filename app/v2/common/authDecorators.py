from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def auth_required(l:list):
    def wraper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] in l:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="You are not authorized to access this resource"), 403
        return decorator
    return wraper

def greater_than():
    def wraper(fn):
        @wraps(fn)
        def decorator(rol, *args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == "admin":
                return fn(rol, *args, **kwargs)
            else:
                return jsonify(msg="You are not authorized to access this resource"), 403
        return decorator
    return wraper

def admin_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["is_administrator"]:
            return fn(*args, **kwargs)
        else:
            return jsonify(msg="Admins only!"), 403

    return decorator