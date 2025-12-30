from flask import Flask, jsonify
import uuid
from jobs import jobs
from downloader import download_url, get_url
import threading
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running"

@app.route("/start", methods=["POST"])
def start_download():
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "starting",
        "completed": 0,
        "total": 0
    }

    # Start downloader in background
    thread = threading.Thread(target=run_downloader, args=(job_id,))
    thread.start()

    return jsonify({
        "message": "Download started",
        "job_id": job_id
    })


@app.route("/progress/<job_id>", methods=["GET"])
def get_progress(job_id):
    if job_id not in jobs:
        return jsonify({"error": "Invalid job id"}), 404
    return jsonify(jobs[job_id])


@app.route("/result/<job_id>", methods=["GET"])
def get_result(job_id):
    if job_id not in jobs:
        return jsonify({"error": "Invalid job id"}), 404

    job = jobs[job_id]

    if job["status"] != "completed":
        return jsonify({
            "message": "Job not completed yet",
            "status": job["status"]
        })

    return jsonify({
        "message": "Download completed",
        "total_files": job["total"],
        "downloaded_files": job["completed"]
    })


def run_downloader(job_id):
    base_url = "https://ncert.nic.in/textbook/pdf/"
    json_file_path = os.path.join(os.getcwd(), "data.json")

    out_dir = "downloads"

    with open(json_file_path, "r") as f:
        data = json.load(f)

    total_files = sum(
        len(books)
        for subjects in data.values()
        for books in subjects.values()
    )

    jobs[job_id]["total"] = total_files
    jobs[job_id]["status"] = "running"

    completed = 0

    for class_num, subjects in data.items():
        for subject, books in subjects.items():
            folder = os.path.join(out_dir, class_num, subject.strip())
            for book in books:
                url = get_url(book.get("code"), base_url)
                filename = book.get("text") + ".zip"
                print("Downloading:", filename)
                success = download_url(url, folder, filename)

                completed += 1
                jobs[job_id]["completed"] = completed

    jobs[job_id]["status"] = "completed"


if __name__ == "__main__":
    app.run(debug=True)
