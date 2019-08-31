$(() => {
    let $course_data = $('.course-data');
    let sViedoUrl = $course_data.data('video-url');
    let sCoverUrl = $course_data.data('cover-url');
    let player = cyberplayer("course-video").setup({
        width: '100%',
        height: 650,
        file: sViedoUrl,
        image: sCoverUrl,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        ak: '334025de9da34118b03f3666fc58232c'
    });
});