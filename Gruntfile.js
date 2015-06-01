module.exports = function(grunt){
    grunt.initConfig({
        jshint: {
            options:{
                globals : {
                    "App": true,
                    "Backbone": true,
                    "$": true,
                    "console": true,
                    "_": true,
                    "JST": true,
                    "addHistoryEvent": true,
                    "setActiveLink": true
                }
            },
            files: ['Gruntfile.js', 'ui/_attachments/script/*.js', 'ui/_attachments/spec/javascripts/*.js']
        },

        jst: {
            compile: {
                options: {
                    processName: function(filepath){
                        name = filepath.split("/").pop();
                        pos = name.indexOf(".html");
                        key = (pos > -1) ? name.substring(0, pos) : name;
                        return key;
                    }
                }

                files : {
                    "ui/_attachments/templates.js": ["ui/_attachments/templates/*.html"]
                }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jst');
    grunt.registerTask('default', ['jshint', 'jst']);
};
