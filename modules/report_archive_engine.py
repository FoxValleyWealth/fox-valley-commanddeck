import os
from datetime import datetime
from shutil import copyfile


# =========================================================
# 📦 Report Archive Engine — v7.7R Final Deployment
# Archives Tactical Command Reports with timestamped filenames
# =========================================================

def archive_report(source_file: str, archive_base: str = "Fox_Valley_Tactical_Command_Report"):
    """
    Archives a PDF Command Report into /archive/reports with
    timestamp-based filename. Ensures no overwrite.
    
    Parameters:
        source_file: Path to original generated PDF.
        archive_base: Prefix for archived PDF files.
    
    Returns:
        archive_path: Path where archived file is stored.
    """

    # Ensure archive directory exists
    archive_dir = os.path.join("archive", "reports")
    os.makedirs(archive_dir, exist_ok=True)

    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_filename = f"{archive_base}_{timestamp}.pdf"
    archive_path = os.path.join(archive_dir, archive_filename)

    # Copy file into archive
    try:
        copyfile(source_file, archive_path)
        return archive_path
    except Exception as e:
        return f"❌ Archive failed: {str(e)}"
