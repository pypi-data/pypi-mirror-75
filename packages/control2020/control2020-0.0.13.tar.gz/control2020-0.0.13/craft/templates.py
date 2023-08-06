index_template = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script type="application/javascript">
            let ep = document.getElementById("_dash-app-content");
            function watcher() {
                if (ep.firstElementChild.childElementCount > 0) {
                    feather.replace();
                } else {
                    setTimeout(watcher, 10);
                }
            }
            watcher();
        </script>
    </body>
</html>

'''

renderer = '''
var renderer = new DashRenderer({
    request_pre: (payload) => {
        // print out payload parameter
        console.log("pre:", payload);
    },
    request_post: (payload, response) => {
        // print out payload and response parameter
        console.log("post_a:", payload);
        console.log("post_b:", response);
    }
})
'''

code_start = '''# Write your code here!
# You can use G, K and H as a TransferFunctions.
# By default here you can use these libraries:
#    numpy as (np)
#    sympy as (sp)
#    control as (ct)
#    control2020 as (ct20)

pid = ct20.design.pid_with_root_placing(G, po=5, ts=10)
print(pid)
'''