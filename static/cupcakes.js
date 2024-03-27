// Define the base URL for the API
const BASE_URL = "http://localhost:5000/api";

/** 
 * Given data about a cupcake, generate HTML representation of the cupcake.
 * @param {Object} cupcake - Cupcake data
 * @returns {string} HTML representation of the cupcake
 */
function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}

/** 
 * Put initial cupcakes on the page.
 */
async function showInitialCupcakes() {
  // Fetch initial cupcakes data from the API
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  // Iterate through each cupcake data and generate HTML for it
  for (let cupcakeData of response.data.cupcakes) {
    // Create a new jQuery object for the cupcake HTML and append it to the cupcakes list
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}

/** 
 * Handle form submission for adding new cupcakes.
 */
$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  // Extract form input values
  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  // Send a POST request to add the new cupcake
  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  // Generate HTML for the new cupcake and append it to the cupcakes list
  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  // Reset the form fields
  $("#new-cupcake-form").trigger("reset");
});

/** 
 * Handle click event for deleting a cupcake.
 */
$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  // Find the closest cupcake div and extract its ID
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");
  // Send a DELETE request to delete the cupcake
  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  // Remove the cupcake HTML from the page
  $cupcake.remove();
});

// Call the function to show initial cupcakes when the page loads
$(showInitialCupcakes);
