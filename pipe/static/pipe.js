
function handleReset() {
    const form = document.getElementById('pipeForm');
    form.reset();
}

function selectRoughnessCoefficient() {
    const material = document.getElementById('pipeMaterial').value;
    const roughnessCoefficient = document.getElementById('roughnessCoefficient');

    switch (material) {
        case 'cast_iron_new':
            roughnessCoefficient.value = '130';
            break;
        case 'cast_iron_10_yr_old':
            roughnessCoefficient.value = '110';
            break;
        case 'cast_iron_20_yr_old':
            roughnessCoefficient.value = '94.5';
            break;
        case 'concrete':
            roughnessCoefficient.value = '120';
            break;
        case 'steel_new':
            roughnessCoefficient.value = '145';
            break;
        case 'plastic':
            roughnessCoefficient.value = '140';
            break;
        case 'fiber':
            roughnessCoefficient.value = '140';
            break;
        default:
            roughnessCoefficient.value = '';
    }
}
document.getElementById('pipeForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data
        console.log(data);
        // Update the form fields with the response data if needed
        // For example:
        // document.getElementById('flow_rate').value = data.flow_rate;
        // document.getElementById('pipeDiameter').value = data.pipe_diameter;
        // document.getElementById('pipeLength').value = data.pipe_length;
        // document.getElementById('roughnessCoefficient').value = data.roughness_coefficient;
        document.getElementById('frictionloss').value = data.friction_loss;

    })
    .catch(error => {
        console.error('Error:', error);
    });
});




// document.getElementById('flowForm').addEventListener('submit', function(event) {
//     event.preventDefault();


// document.addEventListener('DOMContentLoaded', function() {
//     selectRoughnessCoefficient();
// });

