#!/usr/bin/env python3
"""Copy the media shown on the website from the original project folders.

Your projects stay where they are. This script copies only the files listed in
MEDIA below into assets/, converting GIFs/videos to small web-friendly MP4s
(H.264, no audio, max 1280 px wide) and writing a poster image for each video.

Usage:
    python3 tools/sync_media.py            # copy what is missing
    python3 tools/sync_media.py --force    # re-create everything

Requires ffmpeg. To add media: add a line to MEDIA, run the script, then
reference the file from a project in projects/*.md.
"""
import shutil
import subprocess
import sys
from pathlib import Path

DOCS = Path.home() / "Documents"
SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets"

SWE = "ETH/Master/sem_2/gpu2/ShallowWater4PDEonGPU/docs"
HPC4WC = "ETH/Master/sem_2/HPC4WC/HPC4WC_project3_domain_decomp/output"
ASL = "ETH/Master/sem_2/AdvSysLab/Project"
SPGEMM = "ETH/Bachelor/5_sem/DPHPC/Symbolic_SPgeMM/report_source"

# (source relative to ~/Documents, destination relative to assets/, options)
# options: poster=<seconds> time of the poster frame, crop=<ffmpeg crop expr>
MEDIA = [
    # Shallow water / Cleuson dam break
    (f"{SWE}/animations/cleuson_dam_zoom_3d.mp4", "media/cleuson_zoom_3d.mp4",
     {"poster": 9, "crop": "1200:960:230:0"}),
    (f"{SWE}/animations/cleuson_dam_break_5m_3d.mp4", "media/cleuson_valley_3d.mp4",
     {"poster": 12, "crop": "1264:960:156:0"}),
    (f"{SWE}/animations/cleuson_dam_break_5m_2d.mp4", "media/cleuson_2d_5m.mp4",
     {"poster": 9, "crop": "760:1170:260:15"}),
    (f"{SWE}/animations/cleuson_longitudinal_section.mp4", "media/cleuson_section.mp4",
     {"poster": 6}),
    (f"{SWE}/animations/QualityVisualizations/NewTopo1_Gauss.mp4", "media/swe_gauss_3d.mp4",
     {"poster": 8}),
    (f"{SWE}/final_presentation_docs/weak_scaling_plot_dt.png", "img/swe_weak_scaling.png", {}),
    (f"{SWE}/final_presentation_docs/performance_plot.png", "img/swe_bandwidth.png", {}),
    ("ETH/Master/sem_2/gpu2/PDEonGPU_Phase_2.pdf", "pdf/swe_multi_gpu_slides.pdf", {}),
    # HPC4WC
    (f"{HPC4WC}/domain_decompositions.png", "img/hpc4wc_decompositions.png", {}),
    ("ETH/Master/sem_2/HPC4WC/plot_stack_time_16ranks.png", "img/hpc4wc_time_per_iteration.png", {}),
    ("ETH/Master/sem_2/HPC4WC/HPC4WC_project.pdf", "pdf/hpc4wc_domain_decomposition_report.pdf", {}),
    # Semester thesis (only general figures, no model details)
    ("ETH/Master/sem_1/Semester_arbeit/presi/3d_simple_wi.png", "img/semester_3d_wi_final.png", {}),
    # DPHPC symbolic SpGEMM (figures from the report sources)
    (f"{SPGEMM}/performance_plot_with_hash_table.png", "img/spgemm_overlap_methods.png", {}),
    (f"{SPGEMM}/diagrams/BloomFilter_And_Required_Cols.png", "img/spgemm_bloom_filter.png", {}),
    # report_compiled.pdf = report.tex compiled with tectonic (`tectonic -X compile report.tex`)
    (f"{SPGEMM}/report_compiled.pdf", "pdf/dphpc_symbolic_spgemm_report.pdf", {}),
    # Advanced Systems Lab
    (f"{ASL}/docs/out.gif", "media/asl_pedestrians.mp4", {"poster": 6}),
    (f"{ASL}/Final_Report_ASL.pdf", "img/asl_performance.png", {"pdf_page": 7, "pdf_image": 0}),
    (f"{ASL}/Final_Report_ASL.pdf", "pdf/asl_social_force_report.pdf", {}),
    # Bachelor thesis (figure 4.x: WB vs. non-WB perturbation, extracted from the PDF)
    ("ETH/Bachelor/6_sem/Bachelor_thesis/Bachelor_Thesis_Ramura_Gassler.pdf",
     "pdf/bsc_thesis_gassler.pdf", {}),
    ("ETH/Bachelor/6_sem/Bachelor_thesis/Bachelor_Thesis_Ramura_Gassler.pdf",
     "img/bsc_wb_perturbation.png", {"pdf_page": 52, "pdf_image": 0}),
]

MAX_IMG_WIDTH = 1600


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def to_mp4(src, dst, opts):
    filters = []
    if "crop" in opts:
        filters.append(f"crop={opts['crop']}")
    filters.append("scale='min(1280,iw)':-2")
    run(["ffmpeg", "-y", "-i", str(src), "-vf", ",".join(filters),
         "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-an", str(dst)])
    poster = dst.with_suffix(".jpg")
    run(["ffmpeg", "-y", "-ss", str(opts.get("poster", 1)), "-i", str(dst),
         "-frames:v", "1", "-q:v", "3", str(poster)])


def to_png(src, dst, opts):
    if "pdf_page" in opts:
        tmp = dst.parent / "_pdfimg"
        tmp.mkdir(exist_ok=True)
        p = str(opts["pdf_page"])
        run(["pdfimages", "-f", p, "-l", p, "-png", str(src), str(tmp / "i")])
        imgs = sorted(tmp.glob("i-*.png"), key=lambda f: f.stat().st_size, reverse=True)
        src = imgs[opts.get("pdf_image", 0)]
        shutil.copy(src, dst)
        shutil.rmtree(tmp)
        return
    run(["ffmpeg", "-y", "-i", str(src), "-vf", f"scale='min({MAX_IMG_WIDTH},iw)':-2", str(dst)])


def main():
    force = "--force" in sys.argv
    missing = []
    for rel, dest, opts in MEDIA:
        src, dst = DOCS / rel, OUT / dest
        if not src.exists():
            missing.append(rel)
            continue
        if dst.exists() and not force:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        ext = dst.suffix.lower()
        if ext == ".mp4":
            to_mp4(src, dst, opts)
        elif ext == ".png":
            to_png(src, dst, opts)
        else:
            shutil.copy(src, dst)
        print(f"  {dest:42s} {dst.stat().st_size / 1e6:6.2f} MB")
    if missing:
        print("\nNot found (skipped):", *missing, sep="\n  ")


if __name__ == "__main__":
    main()
