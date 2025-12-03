<!-- resources/views/components/error-message.blade.php -->
@props(['message'])

<p class="error-message text-sm text-red-600" {{ $attributes }}>
    {{ $message }}
</p>

@push('styles')
<style>
    .error-message {
        transition: opacity 0.3s ease;
        opacity: 0;
        height: 0;
        overflow: hidden;
    }

    .error-message.show {
        opacity: 1;
        height: auto;
    }
</style>
@endpush