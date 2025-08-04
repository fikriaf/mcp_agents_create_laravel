def generate_route(route_path):
    print("[ROUTE AGENT] Generating route...")
    return f"Route::get('{route_path}', function () {{ return view('dashboard'); }});"
