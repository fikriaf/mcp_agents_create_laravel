def list_components(components):
    print("[COMPONENT AGENT] Listing components...")
    return [f"{c.lower()}.blade.php" for c in components]
