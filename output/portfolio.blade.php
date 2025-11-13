@extends('layouts.app')

@section('content')
@include('components.NavigationBar')
@include('components.HeroSection')
@include('components.AboutSection')
@include('components.SkillsGrid')
@include('components.PortfolioGallery')
@include('components.ExperienceTimeline', [
    'title' => 'Pengalaman',
    'experiences' => [
        [
            'position' => 'Senior Full Stack Developer',
            'company' => 'Tech Innovations Inc.',
            'period' => '2021 - Sekarang',
            'description' => 'Memimpin pengembangan aplikasi web skala enterprise dengan arsitektur microservices.'
        ],
        [
            'position' => 'Full Stack Developer',
            'company' => 'Digital Solutions Ltd.',
            'period' => '2019 - 2021',
            'description' => 'Mengembangkan berbagai proyek web untuk klien enterprise dengan fokus pada performa dan keamanan.'
        ],
        [
            'position' => 'Frontend Developer',
            'company' => 'Creative Agency Studio',
            'period' => '2017 - 2019',
            'description' => 'Membangun antarmuka pengguna yang menarik dan responsif untuk berbagai platform digital.'
        ],
        [
            'position' => 'Junior Web Developer',
            'company' => 'StartUp Hub',
            'period' => '2016 - 2017',
            'description' => 'Bergabung dalam tim pengembangan untuk produk MVP dan aplikasi web startup.'
        ]
    ]
])
@include('components.ContactSection')
@endsection