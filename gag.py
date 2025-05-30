from clipper import run_clipper

if __name__ == "__main__":
    try:
        run_clipper()
    except Exception as e:
        import traceback
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
