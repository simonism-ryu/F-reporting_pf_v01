# -*- coding: utf-8 -*-
"""법인 월간자료 취합 웹앱 (나스 배포판). 업로드->자동병합->웹 다운로드."""
import os
from flask import Flask, request, jsonify, send_file, render_template
import merge_engine as ME

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 80 * 1024 * 1024
ME.ensure()


@app.route("/")
def index():
    return render_template("index.html", month=ME.MONTH)


@app.route("/status")
def status():
    return jsonify(ME.status_all())


@app.route("/upload/<doc_key>", methods=["POST"])
def upload(doc_key):
    if doc_key not in ME.DOCUMENTS:
        return jsonify({"ok": False, "msg": "알 수 없는 문서"}), 400
    doc = ME.DOCUMENTS[doc_key]
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".xlsx"):
        return jsonify({"ok": False, "msg": ".xlsx만 업로드 가능"}), 400
    if doc["mode"] == "single":
        uploader = doc["uploaders"][0]
    else:
        uploader = None
        for e in doc["uploaders"]:
            if e.lower() in f.filename.lower():
                uploader = e
                break
        if not uploader:
            return jsonify({"ok": False, "msg": "파일명에 법인 영문(" + "/".join(doc["uploaders"]) + ") 포함 필요"}), 400
    f.save(os.path.join(ME.inbox_dir(doc_key), uploader + "_" + ME.MONTH + ".xlsx"))
    # 자동 병합: 해당 문서가 모두 제출되면 즉시 병합
    merged = None
    if ME.status_doc(doc_key)["all_done"]:
        merged = ME.run_merge_doc(doc_key)
    return jsonify({"ok": True, "uploader": uploader, "merged": merged,
                    "status": ME.status_all()})


@app.route("/merge/<doc_key>", methods=["POST"])
def merge(doc_key):
    if doc_key not in ME.DOCUMENTS:
        return jsonify({"ok": False, "msg": "알 수 없는 문서"}), 400
    if not ME.status_doc(doc_key)["all_done"]:
        return jsonify({"ok": False, "msg": "아직 모든 제출이 완료되지 않음"}), 400
    return jsonify({"ok": True, "file": ME.run_merge_doc(doc_key), "status": ME.status_all()})


@app.route("/download/<doc_key>")
def download(doc_key):
    lm = ME.latest_master(doc_key)
    if not lm:
        return "병합본이 아직 없습니다.", 404
    return send_file(os.path.join(ME.MASTER_ROOT, lm), as_attachment=True)


@app.route("/reset/<doc_key>", methods=["POST"])
def reset(doc_key):
    d = ME.inbox_dir(doc_key)
    for fn in os.listdir(d):
        if fn.lower().endswith(".xlsx"):
            os.remove(os.path.join(d, fn))
    return jsonify({"ok": True, "status": ME.status_all()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
