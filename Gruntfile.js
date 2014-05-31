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
					keepalive: true
				}
			}
		},

		stylus: {
			compile: {
				options: {
					paths: ['static']
				},
				files: {
					'styles/main.css': 'styles/main.styl'
				}
			}
		},

		watch: {
			css: {
				files: ['static/styles/', 'templates'],
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
	grunt.registerTask('dev', ['connect']);

}