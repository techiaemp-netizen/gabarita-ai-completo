# Deploy script for Render
$apiKey = "rnd_fwSBtmlP5hkuFYbTWxFF83FHidRj"
$repoUrl = "https://github.com/techiaemp-netizen/gabarita-ai-backend"
$serviceName = "gabarita-ai-backend"

# Get owner ID
$ownerResponse = Invoke-RestMethod -Uri "https://api.render.com/v1/owners" -Headers @{"Authorization" = "Bearer $apiKey"}
$ownerId = $ownerResponse[0].owner.id

# Create service payload
$serviceData = @{
    type = "web_service"
    name = $serviceName
    ownerId = $ownerId
    repo = $repoUrl
    branch = "master"
    buildCommand = "pip install -r requirements.txt"
    startCommand = "python src/main.py"
    plan = "free"
    region = "oregon"
    envVars = @(
        @{ key = "PYTHON_VERSION"; value = "3.11.0" }
        @{ key = "PORT"; value = "10000" }
    )
    healthCheckPath = "/health"
}

# Create service
try {
    $response = Invoke-RestMethod -Uri "https://api.render.com/v1/services" -Method POST -Headers @{"Authorization" = "Bearer $apiKey"; "Content-Type" = "application/json"} -Body ($serviceData | ConvertTo-Json -Depth 10)
    Write-Host "Service created successfully!"
    Write-Host "Service ID: $($response.service.id)"
    Write-Host "Service URL: $($response.service.serviceDetails.url)"
} catch {
    Write-Error "Failed to create service: $($_.Exception.Message)"
}