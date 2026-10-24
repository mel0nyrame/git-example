/* =========================================================
   OpenCode 中文介绍 · 交互脚本
   - 主题切换（记忆偏好）
   - 导航：滚动状态 / 进度条 / 当前章节高亮 / 移动端菜单
   - 安装命令：标签切换 + 复制
   - 滚动入场动画
   - FAQ 单开手风琴
   ========================================================= */

(function () {
  'use strict';

  var docEl = document.documentElement;
  var THEME_KEY = 'opencode-intro-theme';
  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- 主题 ---------------- */

  var themeToggle = document.getElementById('themeToggle');

  function syncThemeButton() {
    if (!themeToggle) return;
    var isDark = docEl.dataset.theme === 'dark';
    themeToggle.setAttribute('aria-label', isDark ? '切换为浅色主题' : '切换为深色主题');
    themeToggle.setAttribute('title', isDark ? '切换为浅色主题' : '切换为深色主题');
  }

  function setTheme(theme, persist) {
    docEl.dataset.theme = theme;
    if (persist) {
      try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
    }
    syncThemeButton();
  }

  syncThemeButton();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      setTheme(docEl.dataset.theme === 'dark' ? 'light' : 'dark', true);
    });
  }

  /* ---------------- 导航 ---------------- */

  var nav = document.getElementById('siteNav');
  var progress = document.getElementById('navProgress');
  var burger = document.getElementById('navBurger');
  var navLinks = document.getElementById('navLinks');

  function onScroll() {
    var y = window.scrollY || docEl.scrollTop;
    if (nav) nav.classList.toggle('is-scrolled', y > 8);

    if (progress) {
      var max = docEl.scrollHeight - window.innerHeight;
      var pct = max > 0 ? Math.min(100, (y / max) * 100) : 0;
      progress.style.width = pct + '%';
    }
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      onScroll();
      ticking = false;
    });
  }, { passive: true });
  onScroll();

  /* 移动端菜单 */
  function closeMenu() {
    if (!navLinks || !burger) return;
    navLinks.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', '展开导航');
  }

  if (burger && navLinks) {
    burger.addEventListener('click', function () {
      var open = navLinks.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? '收起导航' : '展开导航');
    });

    navLinks.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 860) closeMenu();
    });
  }

  /* 当前章节高亮 */
  var sections = Array.prototype.slice.call(
    document.querySelectorAll('main section[id]')
  );
  var linkMap = {};

  Array.prototype.forEach.call(document.querySelectorAll('.nav-links a'), function (a) {
    var id = (a.getAttribute('href') || '').replace('#', '');
    if (id) linkMap[id] = a;
  });

  if ('IntersectionObserver' in window && sections.length) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var link = linkMap[entry.target.id];
        if (!link) return;
        Object.keys(linkMap).forEach(function (k) {
          linkMap[k].classList.toggle('is-active', k === entry.target.id);
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });

    sections.forEach(function (s) { sectionObserver.observe(s); });
  }

  /* ---------------- 安装命令标签 + 复制 ---------------- */

  var installBox = document.getElementById('install');

  if (installBox) {
    var tabs = Array.prototype.slice.call(installBox.querySelectorAll('.tab'));
    var panes = Array.prototype.slice.call(installBox.querySelectorAll('.pane'));

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var name = tab.dataset.tab;
        tabs.forEach(function (t) {
          var active = t === tab;
          t.classList.toggle('is-active', active);
          t.setAttribute('aria-selected', String(active));
        });
        panes.forEach(function (p) {
          p.classList.toggle('is-active', p.dataset.pane === name);
        });
      });
    });

    var copyBtn = document.getElementById('copyInstall');
    var copyLabel = copyBtn ? copyBtn.querySelector('span') : null;

    function fallbackCopy(text) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.top = '-1000px';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      return ok;
    }

    function flashCopied(ok) {
      if (!copyBtn || !copyLabel) return;
      var original = '复制';
      copyLabel.textContent = ok ? '已复制' : '请手动复制';
      copyBtn.classList.add('is-done');
      window.setTimeout(function () {
        copyLabel.textContent = original;
        copyBtn.classList.remove('is-done');
      }, 1800);
    }

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var activePane = installBox.querySelector('.pane.is-active');
        if (!activePane) return;
        // 去掉注释行与提示符，只复制命令
        var lines = activePane.textContent.split('\n')
          .map(function (line) { return line.replace(/^\s*\$?\s?/, '').trim(); })
          .filter(function (line) { return line && line.charAt(0) !== '#'; });
        var text = lines.join('\n');

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            flashCopied(true);
          }).catch(function () {
            flashCopied(fallbackCopy(text));
          });
        } else {
          flashCopied(fallbackCopy(text));
        }
      });
    }
  }

  /* ---------------- 滚动入场 ---------------- */

  var revealItems = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

  if (!('IntersectionObserver' in window) || prefersReducedMotion) {
    revealItems.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    // 同组元素依次入场
    revealItems.forEach(function (el) {
      var siblings = el.parentElement
        ? Array.prototype.filter.call(el.parentElement.children, function (c) {
            return c.classList && c.classList.contains('reveal');
          })
        : [el];
      var idx = siblings.indexOf(el);
      if (idx > 0) el.style.transitionDelay = Math.min(idx, 5) * 70 + 'ms';
    });

    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -8% 0px' });

    revealItems.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------------- FAQ：同时只展开一项 ---------------- */

  var detailsList = Array.prototype.slice.call(document.querySelectorAll('.faq-list details'));

  detailsList.forEach(function (item) {
    item.addEventListener('toggle', function () {
      if (!item.open) return;
      detailsList.forEach(function (other) {
        if (other !== item) other.open = false;
      });
    });
  });
})();
