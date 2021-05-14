(defun c:tt1 ()
  (vl-load-com)
  (setq ss (ssget))
  (setq	entlst
	 (mapcar
	   'cadr
	   (vl-remove-if-not
	     '(lambda (x) (= 'ENAME (type (cadr x))))
	     (ssnamex ss)
	   )
	 )
  )
  (setq	redlst
	 (mapcar '(lambda (x)
		    (list (cdr (assoc 10 (entget x)))
			  (cdr (assoc 11 (entget x)))
		    )
		  )
		 (vl-remove-if-not
		   '(lambda (x) (= "中心线" (cdr (assoc 8 (entget x)))))
		   entlst
		 )
	 )
  )
  (setq	ktxtlst
	 (mapcar
	   '(lambda (x)
	      (list (cdr (assoc 10 (entget x)))
		    (cdr (assoc 1 (entget x)))
	      )
	    )
	   (vl-remove-if-not
	     '(lambda (x)
		(and (cdr (assoc 1 (entget x)))
		     (wcmatch (cdr (assoc 1 (entget x))) "K*")
		)
	      )
	     entlst
	   )
	 )
  )
  (setq	stxtlst
	 (mapcar
	   '(lambda (x)
	      (list (cdr (assoc 10 (entget x)))
		    (cdr (assoc 1 (entget x)))
	      )
	    )
	   (vl-remove-if-not
	     '(lambda (x)
		(and (cdr (assoc 1 (entget x)))
		     (wcmatch (cdr (assoc 1 (entget x))) "设计高程*")
		)
	      )
	     entlst
	   )
	 )
  )
  (setq
    yellowlst
     (mapcar
       '(lambda (x) (cons (nth (/ (1- (length x)) 2) x) x))
       (mapcar 'sccf
	       (mapcar
		 '(lambda (x)
		    (mapcar 'cdr
			    (vl-remove-if-not
			      '(lambda (a) (= 10 (car a)))
			      (entget x)
			    )
		    )
		  )
		 (mapcar
		   '(lambda (x)
		      (ssname (ssget "f" x '((8 . "构造物轮廓"))) 0)
		    )
		   redlst
		 )
	       )
       )
     )
  )
  (setq
    nlst (mapcar
	   '(lambda (x)
	      (list (cadar (vl-sort ktxtlst
				    '(lambda (a b)
				       (< (distance (car a) (car x))
					  (distance (car b) (car x))
				       )
				     )
			   )
		    )
		    (cadar (vl-sort stxtlst
				    '(lambda (a b)
				       (< (distance (car a) (car x))
					  (distance (car b) (car x))
				       )
				     )
			   )
		    )
		    x
	      )
	    )
	   yellowlst
	 )
  )
  (setq fileph (getfiled "选择文件" "c/cadd/lisp/" "txt" 2))
  (setq file (open fileph "w"))
  (foreach n
	   (apply
	     'append
	     (mapcar
	       'cltx
	       (vl-sort
		 nlst
		 '(lambda (x y)
		    (<
		      (+ (* 1000 (atof (substr (car x) 2)))
			 (atof
			   (substr (car x)
				   (+ 2 (vl-string-search "+" (car x)))
			   )
			 )
		      )
		      (+ (* 1000 (atof (substr (car y) 2)))
			 (atof
			   (substr (car y)
				   (+ 2 (vl-string-search "+" (car y)))
			   )
			 )
		      )
		    )
		  )
	       )
	     )
	   )
    (write-line n file))
  (close file)
  (princ)
)
(defun sccf (lst)
  (if lst
    (cons (car lst) (sccf (vl-remove (car lst) lst)))
    nil
  )
) 
(defun cltx (lst)
  (append
    (list (car lst)
	  (strcat "X="
		  (rtos (caar (caddr lst)) 2 4)
		  "     "
		  "Y="
		  (rtos (cadar (caddr lst)) 2 4)
		  "     "
		  "Z="
		  (rtos (atof (substr (cadr lst) 12)) 2 4)
	  )
	  (itoa
	    (length
	      (member (car (caddr lst)) (reverse (cdr (caddr lst))))
	    )
	  )
    )
    (mapcar
      '(lambda (x)
	 (strcat "X="
		 (rtos (car x) 2 4)
		 "     "
		 "Y="
		 (rtos (cadr x) 2 4)
		 "     z=0.0000"
	 )
       )
      (member (car (caddr lst)) (reverse (cdr (caddr lst))))
    )
    (list
      (itoa (length (member (car (caddr lst)) (cdr (caddr lst)))))
    )
    (mapcar
      '(lambda (x)
	 (strcat "X="
		 (rtos (car x) 2 4)
		 "     "
		 "Y="
		 (rtos (cadr x) 2 4)
		 "     z=0.0000"
	 )
       )
      (member (car (caddr lst)) (cdr (caddr lst)))
    )
  )
)
(princ "/n——————测试版命令tt——————")