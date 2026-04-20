$(function () {

    // ****************************************
    // Clear the form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#recommendation_id").val("");
        $("#recommendation_source_product_id").val("");
        $("#recommendation_recommended_product_id").val("");
        $("#recommendation_recommendation_type").val("CROSS_SELL");
        $("#recommendation_read_id").val("");
        $("#read_result_id").text("");
        $("#read_result_source_product_id").text("");
        $("#read_result_recommended_product_id").text("");
        $("#read_result_recommendation_type").text("");
        $("#read_result_like_count").text("");
        $("#read_result_created_at").text("");
        $("#read_result_updated_at").text("");
        $("#flash_message").text("");
        $("#search_results_body").empty();
        $("#recommendation_update_id").val("");
        $("#recommendation_update_type").val("CROSS_SELL");
        $("#update_result_id").text("");
        $("#update_result_source_product_id").text("");
        $("#update_result_recommended_product_id").text("");
        $("#update_result_recommendation_type").text("");
        $("#update_result_like_count").text("");
        $("#update_result_created_at").text("");
        $("#update_result_updated_at").text("");
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

    // ****************************************
    // Read a Recommendation by ID
    // ****************************************
    $("#read-btn").click(function () {
        let rec_id = $("#recommendation_read_id").val();

        // Clear previous results
        $("#read_result_id").text("");
        $("#read_result_source_product_id").text("");
        $("#read_result_recommended_product_id").text("");
        $("#read_result_recommendation_type").text("");
        $("#read_result_like_count").text("");
        $("#read_result_created_at").text("");
        $("#read_result_updated_at").text("");
        $("#flash_message").text("");

        if (!rec_id) {
            $("#flash_message").text("Please enter a Recommendation ID");
            return;
        }

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations/${rec_id}`,
            contentType: "application/json"
        });

        ajax.done(function (res) {
            $("#read_result_id").text(res.id);
            $("#read_result_source_product_id").text(res.source_product_id);
            $("#read_result_recommended_product_id").text(res.recommended_product_id);
            $("#read_result_recommendation_type").text(res.recommendation_type);
            $("#read_result_like_count").text(res.like_count);
            $("#read_result_created_at").text(res.created_at);
            $("#read_result_updated_at").text(res.updated_at);
            $("#flash_message").text("Recommendation retrieved successfully!");
        });

        ajax.fail(function (res) {
            if (res.status === 404) {
                $("#flash_message").text(`Recommendation with id '${rec_id}' was not found.`);
            } else {
                let msg = (res.responseJSON && res.responseJSON.message) || "Error reading recommendation";
                $("#flash_message").text(msg);
            }
        });
    });


    // ****************************************
    // Update a Recommendation's Type
    // ****************************************
    $("#update-btn").click(function () {
        let rec_id = $("#recommendation_update_id").val();
        let new_type = $("#recommendation_update_type").val();

        // Clear previous update results
        $("#update_result_id").text("");
        $("#update_result_source_product_id").text("");
        $("#update_result_recommended_product_id").text("");
        $("#update_result_recommendation_type").text("");
        $("#update_result_like_count").text("");
        $("#update_result_created_at").text("");
        $("#update_result_updated_at").text("");
        $("#flash_message").text("");

        if (!rec_id) {
            $("#flash_message").text("Please enter a Recommendation ID");
            return;
        }

        // First GET the existing recommendation so we can send a full payload on PUT
        let getAjax = $.ajax({
            type: "GET",
            url: `/recommendations/${rec_id}`,
            contentType: "application/json"
        });

        getAjax.done(function (existing) {
            let data = {
                "source_product_id": existing.source_product_id,
                "recommended_product_id": existing.recommended_product_id,
                "recommendation_type": new_type
            };

            let putAjax = $.ajax({
                type: "PUT",
                url: `/recommendations/${rec_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });

            putAjax.done(function (res) {
                $("#update_result_id").text(res.id);
                $("#update_result_source_product_id").text(res.source_product_id);
                $("#update_result_recommended_product_id").text(res.recommended_product_id);
                $("#update_result_recommendation_type").text(res.recommendation_type);
                $("#update_result_like_count").text(res.like_count);
                $("#update_result_created_at").text(res.created_at);
                $("#update_result_updated_at").text(res.updated_at);
                $("#flash_message").text("Recommendation updated successfully!");
            });

            putAjax.fail(function (res) {
                if (res.status === 404) {
                    $("#flash_message").text(`Recommendation with id '${rec_id}' was not found.`);
                } else {
                    let msg = (res.responseJSON && res.responseJSON.message) || "Error updating recommendation";
                    $("#flash_message").text(msg);
                }
            });
        });

        getAjax.fail(function (res) {
            if (res.status === 404) {
                $("#flash_message").text(`Recommendation with id '${rec_id}' was not found.`);
            } else {
                let msg = (res.responseJSON && res.responseJSON.message) || "Error updating recommendation";
                $("#flash_message").text(msg);
            }
        });
    });

// ****************************************
// List All Recommendations
// ****************************************
    $("#list_all-btn").click(function () {
        $("#flash_message").text("");
        $("#search_results_body").empty();

        let ajax = $.ajax({
            type: "GET",
            url: "/recommendations",
            contentType: "application/json"
        });

        ajax.done(function (res) {
            let tbody = $("#search_results_body");
            tbody.empty();

            if (!res || res.length === 0) {
                tbody.append(`<tr><td colspan="5">No recommendations found</td></tr>`);
                $("#flash_message").text("No recommendations found");
                return;
            }

            for (let i = 0; i < res.length; i++) {
                let rec = res[i];
                tbody.append(`<tr>
                    <td>${rec.id}</td>
                    <td>${rec.source_product_id}</td>
                    <td>${rec.recommended_product_id}</td>
                    <td>${rec.recommendation_type}</td>
                    <td>${rec.like_count}</td>
                </tr>`);
            }

            $("#flash_message").text("Recommendations listed successfully!");
        });

        ajax.fail(function (res) {
            let msg = (res.responseJSON && res.responseJSON.message) || "Error listing recommendations";
            $("#flash_message").text(msg);
        });
    });
