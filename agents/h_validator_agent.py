def validate(blade_output):
    print("[VALIDATOR] Validating Blade structure...")
    return "@extends" in blade_output and "@section" in blade_output
