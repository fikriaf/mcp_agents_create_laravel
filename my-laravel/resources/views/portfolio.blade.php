<!-- blade content -->
@extends('layouts.app')

@section('content')
    @include('components.Navbar')

    @include('components.HeroSection')

    @include('components.ProfileImage', ['src' => 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'])

    <div class="container mx-auto px-4 py-20">
        <h2 class="text-3xl font-bold text-center mb-12">My Projects</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            @include('components.ProjectCard', [
                'image' => 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'title' => 'Project 1',
                'description' => 'Description for project 1',
                'link' => '#'
            ])

            @include('components.ProjectCard', [
                'image' => 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'title' => 'Project 2',
                'description' => 'Description for project 2',
                'link' => '#'
            ])

            @include('components.ProjectCard', [
                'image' => 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'title' => 'Project 3',
                'description' => 'Description for project 3',
                'link' => '#'
            ])
        </div>
    </div>

    @include('components.AboutSection')

    <section class="py-20 bg-accent">
        <div class="container mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-12">My Skills</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-4xl mx-auto">
                <x-SkillItem>HTML</x-SkillItem>
                <x-SkillItem>CSS</x-SkillItem>
                <x-SkillItem>JavaScript</x-SkillItem>
                <x-SkillItem>React</x-SkillItem>
                <x-SkillItem>Vue.js</x-SkillItem>
                <x-SkillItem>Node.js</x-SkillItem>
                <x-SkillItem>Python</x-SkillItem>
                <x-SkillItem>Django</x-SkillItem>
            </div>
        </div>
    </section>

    @include('components.ContactForm')
@endsection