//You should probably figure out how to do the map reduce thing, then you can do the object buildif thing

$(document).ready(function () {

    $.ajax({
        type: 'GET',
        url: 'http://lain:<13tg597@127.0.0.1:5984/coordinator',
        dataType: 'json',
        success: $(function () {
            var issues = [];
            var counter = 0;
            $.each(item, function (k, v) {
                    counter++;
                    var name = v._attachments
                    var image = 'http://localhost:5984/coordinator/'+v._id+v.file_path.split('/').pop()
                    alert(image);
                    var category
                    var tags
                    var source
                    var related

                    new_issues =
                    {
                        name: name,
                        image: image,
                        category: category,
                        tags: tags,
                        source: source,
                        related: related
                    };

                    issues.push(new_issues);
                });
                $('#number').append(counter);
                var viewModel = {
                    query: ko.observable(''),
                    severity_filter: ko.observable('0')
                };
                viewModel.issues = ko.dependentObservable(function () {

                    var size = issues.size;
                    var search = this.query().toLowerCase();
                    var severity_filter = this.severity_filter();
                    return ko.utils.arrayFilter(issues, function (issue) {
                        var filters = document.getElementsByName('filter');
                        var filter_choice = "";
                        var final = issue.name+issue.tags+issue.category;
                        for (var i = 0; i < filters.length; i++) {
                            if (filters[i].checked) {
                                filter_choice = filters[i].value;
                            }
                        }
                        if (parseInt(issue.severity_u, 10) >
                            parseInt(severity_filter, 10) ||
                            severity_filter == '') {
                            return  final.toLowerCase().indexOf(search) >= 0
                        }
                    });

                }, viewModel);

                ko.applyBindings(viewModel);
            })
        })
    });
