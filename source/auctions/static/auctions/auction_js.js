$(document).ready(function() {
    endpoint = 'latest';
    access_key = '11a1bafe531e2e343d7926875eca5e57';
    symbols = 'USD,CNY'

    $.ajax({
        url: 'http://data.fixer.io/api/' + endpoint + '?access_key=' + access_key + '&symbols=' + symbols,
        dataType: 'jsonp',
        success: function(json) {
            var a = $('#current_bid').text();
            var cny = (json.rates.CNY * a).toFixed(2);
            var usd = (json.rates.USD * a).toFixed(2);
            var b = [usd, cny];
            console.log(b);
            $('#usd').text(usd);
            $('#cny').text(cny);

        }
    });
});