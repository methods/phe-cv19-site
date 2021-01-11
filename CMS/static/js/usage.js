(function($) {
	function getFormattedCurrentDate() {
		var year = new Date().getFullYear();
		var month = new Date().getMonth() + 1;
		var day = new Date().getDate();

		var twoDigit = function (value) {
			return ("0" + (value)).slice(-2);
		};

		return year + "-" + twoDigit(month) + "-" + twoDigit(day);
	}

	function usageCounter() {
		if ($('.download-button').length > 0) {
			$('.download-button').each(function (index, element) {
				$(element).bind('click', function (event) {
					if (crcConfig.usage_logging_url) {
						event.preventDefault();

						var current_date = getFormattedCurrentDate();
						var download_url = new URL(element.href);

						$.ajax({
							type: 'POST',
							url: crcConfig.usage_logging_url,
							crossDomain: true,
							contentType: 'application/json',
							data: "{ \"date\": \"" + current_date + "\", \"key\": \"covid_download:" + download_url.pathname + "\" }",
							dataType: 'json',
							timeout: 1000
						})
							.fail(function (xhr, textStatus, error) {
								console.log("download event error: ");
								console.log(xhr);
								console.log(textStatus);
								console.log(error);
							})
							.always(function () {
								window.location.href = element.href;
							});
					}
				});
			});
		}
	}

	$(document).ready(usageCounter);
	$(document).on('page:load', usageCounter);
}(jQuery));