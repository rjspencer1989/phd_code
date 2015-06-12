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
                    'libs/bootstrap/fonts': 'bootstrap/dist/fonts',
                    'libs/bootstrap/js/bootstrap.js': 'bootstrap/dist/js/bootstrap.js',
                    'libs/bootstrap-datepicker/css/bootstrap-datepicker3.css': 'bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
                    'libs/bootstrap-datepicker/locales': 'bootstrap-datepicker/dist/locales',
                    'libs/bootstrap-datepicker/js/bootstrap-datepicker.js': 'bootstrap-datepicker/dist/js/bootstrap-datepicker.js',
                    'libs/jasmine/jasmine.js': 'jasmine/lib/jasmine-core/jasmine.js',
                    'libs/jasmine/jasmine-html.js': 'jasmine/lib/jasmine-core/jasmine-html.js',
                    'libs/jasmine/boot.js': 'jasmine/lib/jasmine-core/boot.js',
                    'libs/jasmine/jasmine.css': 'jasmine/lib/jasmine-core/jasmine.css',
                    'libs/jasmine-jquery.js': 'jasmine-jquery/lib/jasmine-jquery.js',
                    'libs/jquery.min.js': 'jquery/dist/jquery.min.js',
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
