var alertPlaceholder = document.getElementById('liveAlertPlaceholder')
var alertTrigger = document.getElementById('liveAlertBtn')

function alert(message, type) {
    var wrapper = document.createElement('div')
    wrapper.innerHTML = '<div id="alert-message" class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button class="btn-close fas fa-times"></button></div>'

    alertPlaceholder.append(wrapper)
}

function closeAlert() {
    var alert = document.getElementById('alert-message')
    alert.parentNode.removeChild(alert)
}

if (alertPlaceholder) {
    alertPlaceholder.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-close')) {
            closeAlert()
        }
    })
}