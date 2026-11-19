
import os
import pymupdf

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from Analyze_pdf import analyse_resume_gemini

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def extract_text_from_resume(pdf_path):
    text = ""

    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text() + "\n"

    return text


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    error = None

    if request.method == "POST":

        if "resume" not in request.files:
            error = "Please upload a resume."

        else:
            file = request.files["resume"]

            job_description = request.form.get(
                "job_description", ""
            ).strip()

            if file.filename == "":
                error = "No file selected."

            elif not allowed_file(file.filename):
                error = "Only PDF files are allowed."

            elif not job_description:
                error = "Please enter a job description."

            else:
                filename = secure_filename(file.filename)
                pdf_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], filename
                )

                try:
                    file.save(pdf_path)

                    resume_content = extract_text_from_resume(
                        pdf_path
                    )

                    if not resume_content.strip():
                        raise ValueError(
                            "Could not extract text from the PDF."
                        )

                    result = analyse_resume_gemini(
                        resume_content,
                        job_description
                    )

                except Exception as e:
                    error = f"Analysis failed: {str(e)}"

                finally:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
