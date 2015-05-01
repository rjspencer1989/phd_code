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
            files: ['Gruntfile.js', 'script/*.js', 'spec/javascripts/*.js']
        },

        jst: {
            compile: {
                files : {
                    "./templates.js": ["templates/*.html"]
                }
            }
        },

        concat: {
            dist: {
                src: ['templates.js', 'script/app.js', 'script/utility.js',
                      'script/history.js', 'script/wifi.js',
                      'script/devices.js', 'script/notifications.js',
                      'login.js', 'home.js', 'routes.js', 'startup.js'],
                dest: 'router-ui.js'
            }
        },

        uglify: {
            dist: {
                files: {
                    'router-ui.min.js': 'router-ui.js'
                }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jst');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.registerTask('default', ['jshint', 'jst', 'concat', 'uglify']);
};
