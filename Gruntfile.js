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
                },
                files : {
                    "ui/_attachments/templates.js": ["ui/_attachments/templates/*.html"]
                }
            }
        },

        bowercopy: {
            libs: {
                options: {
                    destPrefix: 'ui/_attachments'
                },

                files: {
                    'libs/backbone.js': 'backbone/backbone.js',
                    'libs/backbone-couchdb.js': 'backbone-couchdb/backbone-couchdb.js',
                    'libs/bootstrap/css/bootstrap.css': 'bootstrap/dist/css/bootstrap.css',
                    'libs/bootstrap': 'bootstrap/dist/fonts',
                    'libs/bootstrap/js/bootstrap.js': 'bootstrap/dist/js/bootstrap.js',
                }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jst');
    grunt.loadNpmTasks('grunt-bowercopy');
    grunt.registerTask('default', ['jshint', 'jst', 'bowercopy']);
};
