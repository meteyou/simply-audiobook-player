<html class="h-full bg-gray-100">
<head>
    <title>{{title or 'Simple Audiobook Player'}}</title>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link href="{{ url('assets', filepath='css/tailwind.css') }}" rel="stylesheet" type="text/css"/>
</head>
<body class="h-full" data-theme="light">
<div class="min-h-full">
    <header class="bg-white shadow">
        <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <h1 class="text-3xl font-bold tracking-tight text-gray-900">Simply Audiobook Player</h1>
        </div>
    </header>

    <main>
        <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
            {{!base}}
        </div>
    </main>
</div>
</body>
</html>
