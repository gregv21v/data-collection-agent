"use strict"

module.exports = function(grunt) {

    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-ngmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-ngdocs');
    grunt.loadNpmTasks('grunt-gh-pages');
    grunt.loadNpmTasks('grunt-karma');
    grunt.loadNpmTasks('grunt-bump');
    grunt.loadNpmTasks('grunt-release');

    grunt.initConfig({
	pkg : grunt.file.readJSON('package.json'),
	templates : [ 'templates/**.html' ],
	build : 'build',
	dist : 'dist',
	src : 'src',
	meta : {
	    banner : '/**\n' + ' * <%= pkg.name %>\n'
		    + ' * @version v<%= pkg.version %> - <%= grunt.template.today("yyyy-mm-dd") %>\n'
		    + ' * @link <%= pkg.homepage %>\n'
		    + ' * @author <%= pkg.author.name %> (<%= pkg.author.email %>)\n'
		    + ' * @license MIT License, http://www.opensource.org/licenses/MIT\n' + ' */\n'
	},
	ngtemplates : {
	    listGroup : {
		cwd : 'src/templates',
		src : '*.html',
		dest : '<%= build %>/templates.js',
		options : {
		    module : 'listGroup',
		    htmlmin : {
			collapseWhitespace : true,
			collapseBooleanAttributes : true
		    }
		}
	    }
	},
	concat : {
	    dist : {
		options : {
		    banner : '(function(window, document) {\n\'use strict\';\n',
		    footer : '\n})(window, document);\n',
		    process : function(src, filepath) {
			return src.replace(/(^|\n)[ \t]*('use strict'|"use strict");?\s*/g, '$1');
		    },
		    stripBanners : true
		},
		src : [ '<%= src %>/*.js', '<%= src%>/filter/*.js', '<%= src%>/service/*.js',
			'<%= src %>/directive/*.js', '<%= build %>/templates.js' ],
		dest : '<%= dist %>/<%= pkg.name %>.js',
	    },
	    banner : {
		options : {
		    banner : '<%= meta.banner %>',
		},
		files : [ {
		    expand : true,
		    cwd : '<%= dist %>',
		    src : '{,*/}*.js',
		    dest : '<%= dist %>'
		} ]
	    }
	},
	ngmin : {
	    dist : {
		files : [ {
		    src : '<%= dist %>/<%= pkg.name %>.js',
		    dest : '<%= dist %>/<%= pkg.name %>.min.js'
		} ]
	    }
	},
	uglify : {
	    dist : {
		files : [ {
		    expand : true,
		    cwd : '<%= dist %>',
		    src : '{,*/}*.js',
		    dest : '<%= dist %>',
		    ext : '.min.js'
		} ]
	    }
	},
	clean : {
	    options : {
		force : true
	    },
	    build : [ '<%= build %>' ],
	    docs : [ '<% dist %>/docs' ]
	},
	copy : {
	    demo : {
		files : [ {
		    expand : true,
		    cwd : '<%= dist %>',
		    src : [ '<%= pkg.name %>.js', '<%= pkg.name %>.min.js', '*.css' ],
		    dest : 'demo/bower_components/<%= pkg.name %>/<%= dist %>'
		} ]
	    },
	    css : {
		files : [ {
		    expand : true,
		    cwd : 'src/css',
		    src : [ '*.css' ],
		    dest : '<%= dist %>'
		} ]
	    }
	},
//	ngdocs : {
//	    options : {
//		dest : '<%= dist %>/docs',
//		scripts : [ 'http://cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular.js',
//			'http://cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular-route.min.js',
//			'http://cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular-animate.min.js',
//			// '../angular-list-group.min.js'
//			'../angular-list-group.js' ],
//		// html5Mode: true,
//		startPage : '/api',
//		title : 'Angular List Group',
//	    },
//	    api : {
//		src : [ 'src/**/*.js' ],
//		title : 'API Documentation'
//	    }
//	},
	karma : {
	    unit : {
		configFile : 'karma.conf.js'
	    }
	},
	'gh-pages' : {
	    options : {
			base : 'demo',
	    },
	    src : [ 'index.html', 'app/**', 'bower_components/**', 'partials/**', 'style/**' ]
	},
	release: {
	    options: {
	      additionalFiles: ['bower.json'],
	      npm: false
	    }
	}
    });

    grunt.registerTask('build', [ 'ngtemplates', 'concat:dist', 'ngmin:dist', 'copy:css', 'clean:build' ]);
    grunt.registerTask('docs', [ 'clean:docs', 'ngdocs' ]);
    grunt.registerTask('build:demo', [ 'build', 'copy:demo' ]);
    grunt.registerTask('deploy:demo', [ 'gh-pages' ]);
    grunt.registerTask('test', [ 'karma' ]);
};