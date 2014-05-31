/**
 * Created by Evgeny Chuvelev on 31/05/14.
 * e.chuvelev@gmail.com
 */

module.exports = function (grunt) {


	// Config
	grunt.initConfig({

		connect: {
			server: {
				options: {
					host: 'localhost',
					port: 8001,
					base: '.',
				}
			}
		},

		stylus: {
			compile: {
				options: {
					paths: ['static/styles'],
				},
				files: {
					'main.css': 'main.styl'
				}
			}
		},

		watch: {
			css: {
				files: ['static/styles/*'],
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
	grunt.loadNpmTasks('grunt-contrib-watch');

	// Tasks
	grunt.registerTask('dev', ['connect', 'watch']);

}