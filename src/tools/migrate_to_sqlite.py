#!/usr/bin/env python3
"""
Migration tool for converting YAML files to SQLite database.

Usage:
    python -m src.tools.migrate_to_sqlite \
        --resumes-root ./resumes \
        --jobs-root ./jobs \
        --db-path ./src/db/resumai.db

Options:
    --resumes-root PATH  Path to resumes directory (default: ./resumes)
    --jobs-root PATH     Path to jobs directory (default: ./jobs)
    --db-path PATH       Path to SQLite database (default: ./src/db/resumai.db)
    --dry-run            Show what would be imported without making changes
    --verbose            Show detailed output
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.db import init_db, get_connection, close_connection
from src.db.schema import get_database_stats, get_all_tables
from src.services.yaml_import_service import YamlImportService


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_section(text: str) -> None:
    """Print a formatted section header."""
    print(f"\n--- {text} ---")


def validate_paths(args) -> bool:
    """Validate input paths exist."""
    valid = True

    if not args.resumes_root.exists():
        print(f"ERROR: Resumes directory not found: {args.resumes_root}")
        valid = False

    if not args.jobs_root.exists():
        print(f"ERROR: Jobs directory not found: {args.jobs_root}")
        valid = False

    return valid


def count_yaml_files(directory: Path, pattern: str = "*.yaml") -> int:
    """Count YAML files in a directory."""
    return len(list(directory.glob(pattern)))


def count_job_folders(jobs_root: Path) -> dict:
    """Count job folders by phase."""
    phases = [
        "1_Queued",
        "2_Data_Generated",
        "3_Docs_Generated",
        "4_Applied",
        "5_FollowUp",
        "6_Interviewing",
        "7_Negotiating",
        "8_Accepted",
        "Skipped",
        "Expired",
        "Errored",
    ]

    counts = {}
    for phase in phases:
        phase_dir = jobs_root / phase
        if phase_dir.exists():
            # Count directories with job.yaml
            count = 0
            for folder in phase_dir.iterdir():
                if folder.is_dir() and (folder / "job.yaml").exists():
                    count += 1
            counts[phase] = count

    return counts


def analyze_source(args) -> dict:
    """Analyze source data before migration."""
    analysis = {
        "resumes": count_yaml_files(args.resumes_root),
        "jobs_by_phase": count_job_folders(args.jobs_root),
    }

    analysis["total_jobs"] = sum(analysis["jobs_by_phase"].values())

    return analysis


def run_migration(args) -> dict:
    """Run the migration process."""
    results = {
        "resumes_imported": 0,
        "jobs_imported": {},
        "errors": [],
        "start_time": datetime.now(),
    }

    try:
        # Initialize database
        print_section("Initializing database")
        conn = init_db(args.db_path)
        print(f"Database created at: {args.db_path}")

        # Create import service
        import_service = YamlImportService(conn)

        # Import resumes
        print_section("Importing resumes")
        imported_resumes = import_service.import_all_resumes(args.resumes_root)
        results["resumes_imported"] = len(imported_resumes)

        for slug in imported_resumes:
            if args.verbose:
                print(f"  Imported resume: {slug}")

        print(f"Imported {len(imported_resumes)} resumes")

        # Import jobs
        print_section("Importing jobs")
        job_counts = import_service.import_all_jobs(args.jobs_root)
        results["jobs_imported"] = job_counts

        total_jobs = sum(job_counts.values())
        print(f"Imported {total_jobs} jobs across {len(job_counts)} phases")

        if args.verbose:
            for phase, count in job_counts.items():
                print(f"  {phase}: {count} jobs")

    except Exception as e:
        results["errors"].append(str(e))
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        results["end_time"] = datetime.now()
        results["duration"] = results["end_time"] - results["start_time"]
        close_connection()

    return results


def verify_migration(args) -> dict:
    """Verify the migration was successful."""
    print_section("Verifying migration")

    conn = get_connection(args.db_path)

    try:
        stats = get_database_stats(conn)
        tables = get_all_tables(conn)

        # Key counts to verify
        verification = {
            "tables_created": len(tables),
            "resumes": stats.get("resumes", 0),
            "jobs": stats.get("jobs", 0),
            "resume_contacts": stats.get("resume_contacts", 0),
            "resume_skills": stats.get("resume_skills", 0),
            "resume_companies": stats.get("resume_companies", 0),
            "job_tags": stats.get("job_tags", 0),
            "job_subcontent_contacts": stats.get("job_subcontent_contacts", 0),
            "job_subcontent_skills": stats.get("job_subcontent_skills", 0),
            "job_subcontent_companies": stats.get("job_subcontent_companies", 0),
            "job_artifacts": stats.get("job_artifacts", 0),
        }

        print(f"Tables created: {verification['tables_created']}")
        print(f"Resumes: {verification['resumes']}")
        print(f"Jobs: {verification['jobs']}")

        if args.verbose:
            print("\nDetailed table counts:")
            for table, count in sorted(stats.items()):
                print(f"  {table}: {count}")

        # Check phase distribution
        cursor = conn.cursor()
        cursor.execute("SELECT phase, COUNT(*) as count FROM jobs GROUP BY phase")
        phase_counts = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()

        print("\nJobs by phase:")
        for phase, count in sorted(phase_counts.items()):
            print(f"  {phase}: {count}")

        verification["phase_counts"] = phase_counts

        return verification

    finally:
        close_connection()


def generate_report(analysis: dict, results: dict, verification: dict) -> None:
    """Generate a migration report."""
    print_header("MIGRATION REPORT")

    print_section("Source Data")
    print(f"Resumes found: {analysis['resumes']}")
    print(f"Jobs found: {analysis['total_jobs']}")
    for phase, count in analysis["jobs_by_phase"].items():
        print(f"  {phase}: {count}")

    print_section("Migration Results")
    print(f"Resumes imported: {results['resumes_imported']}")
    total_imported = sum(results["jobs_imported"].values())
    print(f"Jobs imported: {total_imported}")
    print(f"Duration: {results['duration']}")

    if results["errors"]:
        print_section("Errors")
        for error in results["errors"]:
            print(f"  ERROR: {error}")

    print_section("Verification")
    print(f"Database tables: {verification['tables_created']}")
    print(f"Resumes in DB: {verification['resumes']}")
    print(f"Jobs in DB: {verification['jobs']}")

    # Check for discrepancies
    discrepancies = []

    if analysis["resumes"] != verification["resumes"]:
        discrepancies.append(
            f"Resume count mismatch: expected {analysis['resumes']}, got {verification['resumes']}"
        )

    if analysis["total_jobs"] != verification["jobs"]:
        discrepancies.append(
            f"Job count mismatch: expected {analysis['total_jobs']}, got {verification['jobs']}"
        )

    if discrepancies:
        print_section("Discrepancies")
        for d in discrepancies:
            print(f"  WARNING: {d}")
    else:
        print("\nMigration completed successfully with no discrepancies.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate ResumAI from YAML files to SQLite database"
    )

    parser.add_argument(
        "--resumes-root",
        type=Path,
        default=Path("./resumes"),
        help="Path to resumes directory (default: ./resumes)",
    )

    parser.add_argument(
        "--jobs-root",
        type=Path,
        default=Path("./jobs"),
        help="Path to jobs directory (default: ./jobs)",
    )

    parser.add_argument(
        "--db-path",
        type=Path,
        default=Path("./src/db/resumai.db"),
        help="Path to SQLite database (default: ./src/db/resumai.db)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without making changes",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )

    args = parser.parse_args()

    print_header("ResumAI YAML to SQLite Migration")
    print(f"Resumes root: {args.resumes_root}")
    print(f"Jobs root: {args.jobs_root}")
    print(f"Database path: {args.db_path}")

    # Validate paths
    if not validate_paths(args):
        sys.exit(1)

    # Analyze source data
    print_section("Analyzing source data")
    analysis = analyze_source(args)
    print(f"Found {analysis['resumes']} resumes")
    print(f"Found {analysis['total_jobs']} jobs")

    if args.verbose:
        for phase, count in analysis["jobs_by_phase"].items():
            print(f"  {phase}: {count}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made. Use without --dry-run to perform migration.")
        return

    # Confirm if database exists
    if args.db_path.exists():
        response = input(f"\nDatabase {args.db_path} already exists. Overwrite? [y/N] ")
        if response.lower() != "y":
            print("Aborted.")
            sys.exit(0)
        args.db_path.unlink()

    # Run migration
    results = run_migration(args)

    # Verify migration
    verification = verify_migration(args)

    # Generate report
    generate_report(analysis, results, verification)


if __name__ == "__main__":
    main()
