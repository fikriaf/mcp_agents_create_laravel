<!-- blade content -->
@extends('layouts.app')

@section('content')
    @include('components.Navbar')
    @include('components.HeroSection')
    @include('components.AboutSection')
    @include('components.SkillsSection')
    @include('components.ProjectsSection')
    @include('components.TestimonialsSection')
    @include('components.ContactSection')
    @include('components.Footer')
@endsection