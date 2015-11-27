module.exports = function(grunt){
    grunt.initConfig({
        jshint: {
            options:{
                globals : {
                    "Backbone": true,
                    "$": true,
                    "_": true,
                    "JST": true
                }
            },
            files: ['Gruntfile.js', 'ui/_attachments/script/*.js', 'ui/_attachments/spec/javascripts/*.js']
        },

        jst: {
            compile: {
                options: {
                    processName: function(filepath){
                        name = filepath.split("/").pop();
                        var pos = name.indexOf(".html");
                        var key = (pos > -1) ? name.substring(0, pos) : name;
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
                    'libs/bootstrap/fonts': 'bootstrap/dist/fonts',
                    'libs/bootstrap/js/bootstrap.min.js': 'bootstrap/dist/js/bootstrap.min.js',
                    'libs/jasmine/jasmine.js': 'jasmine/lib/jasmine-core/jasmine.js',
                    'libs/jasmine/jasmine-html.js': 'jasmine/lib/jasmine-core/jasmine-html.js',
                    'libs/jasmine/boot.js': 'jasmine/lib/jasmine-core/boot.js',
                    'libs/jasmine/jasmine.css': 'jasmine/lib/jasmine-core/jasmine.css',
                    'libs/jasmine-jquery.js': 'jasmine-jquery/lib/jasmine-jquery.js',
                    'libs/jquery.min.js': 'jquery/dist/jquery.min.js',
                    'libs/jquery-ui.min.js': 'jquery-ui/jquery-ui.min.js',
                    'libs/jquery-ui.min.css': 'jquery-ui/themes/smoothness/jquery-ui.min.css',
                    'libs/jquery.json.min.js': 'jquery-json/dist/jquery.json.min.js',
                    'libs/underscore-min.js': 'underscore/underscore-min.js'
                }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jst');
    grunt.loadNpmTasks('grunt-bowercopy');
    grunt.registerTask('default', ['jshint', 'jst', 'bowercopy']);
};
