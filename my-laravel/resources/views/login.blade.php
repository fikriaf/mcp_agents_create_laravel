<!-- blade content -->
@extends('layouts.app')
@section('content')
@include('components.headersection')
@include('components.loginform')
@include('components.footersection')
@include('components.errormessage', ['message' => 'An error occurred. Please try again.'])
@endsection