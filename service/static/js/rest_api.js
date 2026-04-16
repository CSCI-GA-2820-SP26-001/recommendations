$(function () {

    // ****************************************
    // Clear the form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#recommendation_id").val("");
        $("#recommendation_source_product_id").val("");
        $("#recommendation_recommended_product_id").val("");
        $("#recommendation_recommendation_type").val("CROSS_SELL");
        $("#flash_message").text("");
        $("#search_results_body").empty();
    });

    // ****************************************
    // Create a Recommendation
    // ****************************************
    $("#create-btn").click(function () {
        let source_product_id = parseInt($("#recommendation_source_product_id").val());
        let recommended_product_id = parseInt($("#recommendation_recommended_product_id").val());
        let recommendation_type = $("#recommendation_recommendation_type").val();

        let data = {
            "source_product_id": source_product_id,
            "recommended_product_id": recommended_product_id,
            "recommendation_type": recommendation_type
        };

        $("#flash_message").text("");

        let ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data)
        });

        ajax.done(function (res) {
            $("#recommendation_id").val(res.id);
            $("#flash_message").text("Recommendation created successfully!");
            let tbody = $("#search_results_body");
            tbody.empty();
            tbody.append(`<tr>
                <td>${res.id}</td>
                <td>${res.source_product_id}</td>
                <td>${res.recommended_product_id}</td>
                <td>${res.recommendation_type}</td>
                <td>${res.like_count}</td>
            </tr>`);
        });

        ajax.fail(function (res) {
            $("#flash_message").text(res.responseJSON.message || "Error creating recommendation");
        });
    });

});