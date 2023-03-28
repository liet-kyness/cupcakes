const API_BASE_URL = 'http://localhost:5555/api'

function renderHTML(cupcake) {
    return `
        <div data-cupcake-id="${cupcake.id}">
            <li>
                ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
                <button class="delete-button">X</button>
            </li>
            <img style="height: 60px" src="${cupcake.image}" class="cupcake-image">
        </div>`;
};

async function showCupcakes() {
    const response = await axios.get(`${API_BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(renderHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    };
};

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
  
    await axios.delete(`${API_BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
  });


  $("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
  
    const newCupcakeResponse = await axios.post(`${API_BASE_URL}/cupcakes`, {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(renderHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
  });


  $(showCupcakes);


