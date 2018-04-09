var gulp         = require('gulp'),
    exec         = require('child_process').exec;
    plumber      = require('gulp-plumber'),
    concat       = require('gulp-concat'),
    browserify   = require('browserify'),
	sass 		 = require('gulp-sass'),
    babelify     = require('babelify'),
    source       = require('vinyl-source-stream'),
    buffer       = require('vinyl-buffer'),
    uglifyify    = require('uglifyify'),
    uglify       = require('gulp-uglify'),
    notify       = require('gulp-notify'),
    envify       = require('envify');

var dirs = {
	dev:'./ui/static/dev',
    prod:'./ui/static/public'
}

var dependencies = [
    'react',
    'react-dom'
];

gulp.task('scss_task', function () {
    gulp.src(dirs.dev+'/css/*.scss')
    .pipe(plumber())
    .pipe(concat('styles.css'))
    .pipe(sass())
    .pipe(plumber.stop()) 
    .pipe(gulp.dest(dirs.prod+'/css'))
    .pipe(notify("Save Styles Sass"))
});

gulp.task('js_task',function(){
    browserify({
        entries: [ dirs.dev+'/js/app.js'],
        debug: true
    })
    .transform("babelify", {presets: ["env", "react"]})
    //Set NODE_ENV: 'production' for production compilation
    .transform("envify", {global: true, _: 'purge', NODE_ENV: 'development'})
    .transform("uglifyify", {global: true})
	.bundle()
    .pipe(source('bundle.js'))
    //Uncomment both lines for production compilation.
    .pipe(buffer())
	.pipe(uglify())
	.pipe(gulp.dest(dirs.prod+'/js'))
	.pipe(notify("Save Scripts"))
});

gulp.task('collectstatic', function () {
    exec("python manage.py collectstatic --noinput", function (err, stdout, stderr) {
        console.log(stdout);
        console.log(stderr);
    });
});

gulp.task('watch', ['scss_task', 'js_task'], function() {
    gulp.watch(dirs.dev+'/css/*.scss', ['scss_task']);
    //gulp.watch(dirs.dev+'/js/*.js', ['js_task']);
    gulp.watch(dirs.dev+'/js/**/*', ['js_task']);
    gulp.watch(dirs.prod+'/**/**/*', ['collectstatic']);
});

gulp.task('default', ['watch']);