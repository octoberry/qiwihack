module.exports = function (grunt) {


	// Config
	grunt.initConfig({

		connect: {
			server: {
				options: {
					host: 'localhost',
					port: 8001,
					base: '.',
//					keepalive: true
				}
			}
		},

//        'bower': {
//            options: {
//                color:       true,
//                production:  false,
//                directory:   "static/bower_components"
//            }
//        },

		stylus: {
			compile: {
                options: {
                    path: ['/static/styles'],
                    compress: false,
                    import: grunt.file.expand('/static/styles/mixins.styl')
                },
				files: {
                    'static/build/main.css': 'static/styles/main.styl'
				}
			}
		},

		watch: {
			css: {
				files: ['static/styles/*.styl'],
				tasks: ['stylus'],
				options: {
					livereload: true,
					port: 8001
				}
			}
		}


	});

	// Plugins
	grunt.loadNpmTasks('grunt-contrib-stylus');
	grunt.loadNpmTasks('grunt-contrib-connect');
//    grunt.loadNpmTasks('grunt-bower-install-simple');
	grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib');

	// Tasks
	grunt.registerTask('dev', ['connect','watch']);
    grunt.registerTask('bower-install', [ 'bower' ]);
}