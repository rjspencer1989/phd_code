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
                src: ['templates.js', 'script/*.js'],
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
    grunt.registerTask('default', ['jshint', 'jst', 'concat']);
};
