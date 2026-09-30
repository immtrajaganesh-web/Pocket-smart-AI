import json
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import firebase_admin
from firebase_admin import credentials, firestore
from app.config import get_settings

_db = None
_initialized = False

def init_firebase() -> Optional[firestore.Client]:
    global _db, _initialized
    if _initialized:
        return _db

    settings = get_settings()
    cred = None

    # 1. From JSON string in environment variable (Ideal for Vercel)
    service_account_raw = (
        os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON") or 
        settings.firebase_service_account_json or 
        ""
    ).strip()

    if service_account_raw:
        try:
            cert_dict = json.loads(service_account_raw)
            cred = credentials.Certificate(cert_dict)
        except Exception as e:
            print(f"[Firebase] Warning: Failed to parse FIREBASE_SERVICE_ACCOUNT_JSON: {e}")

    # 2. From file path (Ideal for local development)
    if not cred:
        cred_path = (
            os.environ.get("FIREBASE_CREDENTIALS_PATH") or 
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or
            settings.firebase_credentials_path or 
            "firebase_credentials.json"
        )
        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
            except Exception as e:
                print(f"[Firebase] Warning: Failed to load credentials from {cred_path}: {e}")

    # 3. From Application Default Credentials / Project ID
    project_id = os.environ.get("FIREBASE_PROJECT_ID") or settings.firebase_project_id
    if not cred and project_id:
        try:
            cred = credentials.ApplicationDefault()
        except Exception:
            pass

    if cred or (project_id and not firebase_admin._apps):
        try:
            options = {"projectId": project_id} if project_id else {}
            if not firebase_admin._apps:
                if cred:
                    firebase_admin.initialize_app(cred, options)
                else:
                    firebase_admin.initialize_app(options=options)
            _db = firestore.client()
            _initialized = True
            print("[+] Firebase Firestore Database successfully connected!")
            return _db
        except Exception as e:
            print(f"[Firebase] Initialization failed: {e}")

    _initialized = True
    return None

def get_firestore_db() -> Optional[firestore.Client]:
    if not _initialized:
        return init_firebase()
    return _db

def is_firebase_configured() -> bool:
    return get_firestore_db() is not None

# ----------------- User Operations -----------------

def fb_get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    db = get_firestore_db()
    if not db:
        return None
    users_ref = db.collection("users").where("email", "==", email.lower().strip()).limit(1).stream()
    for doc in users_ref:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None

def fb_get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    db = get_firestore_db()
    if not db:
        return None
    doc = db.collection("users").document(str(user_id)).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None

def fb_create_user(name: str, email: str, password_hash: str) -> Dict[str, Any]:
    db = get_firestore_db()
    if not db:
        raise RuntimeError("Firebase is not configured")
    email_clean = email.lower().strip()
    user_ref = db.collection("users").document()
    user_data = {
        "name": name.strip(),
        "email": email_clean,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    user_ref.set(user_data)
    user_data["id"] = user_ref.id
    return user_data

# ----------------- Recommendation Operations -----------------

def fb_save_recommendation(user_id: str, planner: str, title: str, request_data: dict, result_data: dict) -> Dict[str, Any]:
    db = get_firestore_db()
    if not db:
        raise RuntimeError("Firebase is not configured")
    rec_ref = db.collection("recommendations").document()
    doc_data = {
        "user_id": str(user_id),
        "planner": planner,
        "title": title,
        "request_data": request_data,
        "result_data": result_data,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    rec_ref.set(doc_data)
    return {"id": rec_ref.id, "message": "Plan saved to Firebase successfully"}

def fb_get_recommendation(rec_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    db = get_firestore_db()
    if not db:
        return None
    doc = db.collection("recommendations").document(str(rec_id)).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    if str(data.get("user_id")) != str(user_id):
        return None
    data["id"] = doc.id
    return data

def fb_delete_recommendation(rec_id: str, user_id: str) -> bool:
    db = get_firestore_db()
    if not db:
        return False
    doc_ref = db.collection("recommendations").document(str(rec_id))
    doc = doc_ref.get()
    if not doc.exists:
        return False
    if str(doc.to_dict().get("user_id")) != str(user_id):
        return False
    doc_ref.delete()
    return True

def fb_get_user_history(user_id: str) -> List[Dict[str, Any]]:
    db = get_firestore_db()
    if not db:
        return []
    recs_ref = db.collection("recommendations").where("user_id", "==", str(user_id)).stream()
    items = []
    for doc in recs_ref:
        d = doc.to_dict()
        res = d.get("result_data") or {}
        items.append({
            "id": doc.id,
            "planner": d.get("planner", "home"),
            "title": d.get("title", "Budget Plan"),
            "created_at": d.get("created_at"),
            "summary": res.get("summary", ""),
            "budget": res.get("budget", 0),
            "currency": res.get("currency", "INR")
        })
    # Sort in memory descending by created_at
    items.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
    return items
