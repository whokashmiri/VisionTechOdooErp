
function Update-OdooModule {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Module,

        [switch]$Install
    )

    $Flag = "-u"

    if ($Install) {
        $Flag = "-i"
    }

    docker compose stop odoo

    docker compose run --rm --no-deps odoo odoo `
        -d configllc `
        $Flag $Module `
        --stop-after-init `
        --no-http

    $Result = $LASTEXITCODE

    docker compose up -d odoo

    if ($Result -ne 0) {
        throw "Module operation failed: $Module"
    }

    Write-Host "Module operation completed: $Module"
}
