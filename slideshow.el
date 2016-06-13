(global-set-key (kbd "<f11>") 'prev-slide)
(global-set-key (kbd "<f12>") 'next-slide)

(setq slide-index 0)

(setq slide-filenames [
    "template.py"
    "factorial.toot"
    "parse.py"
    "parse_example.py"
    "abstract_syntax.py"
    "toot0.py"
    "toot1_split_env.py"
    "toot2_inline_env.py"
    "toot3_staged_env.py"
    "toot4_eagerly_analyze.py"
    "toot5_eager_all_the_way.py"
    "toot6_stacky.py"
    "stack_example.py"
    "toot7_chained.py"
    "toot8_encoded.py"
])

(defun prev-slide ()
  (interactive)
  (setq slide-index (- slide-index 1))
  (show-slide))

(defun next-slide ()
  (interactive)
  (setq slide-index (+ slide-index 1))
  (show-slide))

(defun show-slide ()
  (find-file (concat "/home/darius/git/toot/"
                     (aref slide-filenames (mod slide-index (length slide-filenames))))))
