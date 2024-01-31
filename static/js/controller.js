function gettime() {
	$.ajax({
		url: "/time",
		timeout: 10000,
		success: function(data) {
			$("#time").html(data)
		},
		error: function(xhr, type, errorThrown) {

		}
	});
}

function get_today_sum_data() {
	$.ajax({
		url: "/todaysum",
		success: function(data) {
			$(".num h1").eq(0).html(data.post);
			$(".num h1").eq(1).html(data.comment);
			$(".num h1").eq(2).html(data.valence);
			$(".num h1").eq(3).html(data.arousal);
			$(".num h1").eq(4).html(data.ups);
			$(".num h1").eq(5).html(data.downs);
		},
		error: function(xhr, type, errorThrown) {
			// Handle error if needed
		}
	});
}

function get_engagement_data() {
    $.ajax({
        url: "/engagement",
        success: function(data) {
            option_eg.series[0].data = data.comments;
            option_eg.series[1].data = data.ups;
            option_eg.series[2].data = data.downs;
            ec_eg.setOption(option_eg);
        },
        error: function(xhr, type, errorThrown) {
            // Handle error if needed
        }
    });
}


get_engagement_data()
gettime()
get_today_sum_data()
setInterval(gettime, 1000)
setInterval(get_today_sum_data, 1000*60*1)
setInterval(get_engagement_data, 1000*60*1)
