module.exports = function(grunt){
    grunt.initConfig({
        jshint: {
            options:{
                globals : {
                    "App": true,
                    "Backbone": true
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
        }
    });
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jst');
    grunt.registerTask('default', ['jshint', 'jst']);
};
