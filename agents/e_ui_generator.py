def generate_blade(layout):
    print("[UI GENERATOR] Generating Blade view...")
    return f"""@extends('{layout["extends"]}')

@section('sidebar')
  @include('{layout["sections"]["sidebar"]}')
@endsection

@section('content')
  @include('{layout["sections"]["content"]}')
@endsection
"""
