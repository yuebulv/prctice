(defun c:ttt ()
  (vl-load-com)
  (princ "\n请选择要提取数据的图形：")
  (setq ss (ssget))
  (setq	entlst '()
	n -1
  )
  (while (setq ent (ssname ss (setq n (1+ n))))
    (cond ((= "LWPOLYLINE" (cdr (assoc 0 (entget ent))))
	   (setq entlst
		  (cons
		    (append
		      (list
			2
			(if
			  (= 256
			     (vla-get-Color (vlax-ename->vla-object ent))
			  )
			   (cdr
			     (assoc
			       62
			       (tblsearch "layer"
					  (cdr (assoc 8 (entget ent)))
			       )
			     )
			   )
			   (vla-get-Color (vlax-ename->vla-object ent))
			)
		      )
		      (mapcar 'cdr
			      (vl-remove-if-not
				'(lambda (x) (= 10 (car x)))
				(entget ent)
			      )
		      )
		    )
		    entlst
		  )
	   )
	  )
	  ((= "LINE" (cdr (assoc 0 (entget ent))))
	   (setq entlst
		  (cons
		    (list
		      3
		      (if
			(= 256 (vla-get-Color (vlax-ename->vla-object ent)))
			 (cdr
			   (assoc
			     62
			     (tblsearch "layer" (cdr (assoc 8 (entget ent))))
			   )
			 )
			 (vla-get-Color (vlax-ename->vla-object ent))
		      )
		      (cdr (assoc 10 (entget ent)))
		      (cdr (assoc 11 (entget ent)))
		    )
		    entlst
		  )
	   )
	  )
	  ((= "TEXT" (cdr (assoc 0 (entget ent))))
	   (if (not (wcmatch (cdr (assoc 1 (entget ent))) "*比*例*"))
	     (setq entlst (cons	(list 1
				      (cdr (assoc 1 (entget ent)))
				      (cdr (assoc 10 (entget ent)))
				)
				entlst
			  )
	     )
	   )
	  )
    )
  )
  (setq	redpt
	 (mapcar 'caddr
		 (vl-remove-if-not
		   '(lambda (x) (and (= 3 (car x)) (= 1 (cadr x))))
		   entlst
		 )
	 )
  )
  (setq
    nentlst
     (mapcar
       '(lambda	(y)
	  (mapcar
	    '(lambda (x)
	       (if (= 'STR (type (caar x)))
		 (mapcar
		   'car
		   (vl-sort
		     (vl-sort
		       x
		       '(lambda (a b) (> (cadr (last a)) (cadr (last b))))
		     )
		     '(lambda (a b) (< (car (last a)) (car (last b))))
		   )
		 )
		 (vl-sort
		   (vl-sort
		     x
		     '(lambda (a b) (> (cadr (last a)) (cadr (last b))))
		   )
		   '(lambda (a b) (< (car (last a)) (car (last b))))
		 )
	       )
	     )
	    y
	  )
	)
       (mapcar '(lambda	(x)
		  (amllst (vl-sort x '(lambda (a b) (< (car a) (car b)))))
		)
	       (amllst
		 (mapcar
		   '(lambda (x)
		      (cons (car
			      (vl-sort (if (= 1 (car x))
					 (vl-remove-if
					   '(lambda (n)
					      (< (cadr n)
						 (cadr (last x))
					      )
					    )
					   redpt
					 )
					 redpt
				       )
				       '(lambda	(a b)
					  (< (distance (last x) a)
					     (distance (last x) b)
					  )
					)
			      )
			    )
			    x
		      )
		    )
		   entlst
		 )
	       )
       )
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
		 nentlst
		 '(lambda (x y)
		    (<
		      (+ (* 1000 (atof (substr (caar x) 2)))
			 (atof
			   (substr (caar x)
				   (+ 2 (vl-string-search "+" (caar x)))
			   )
			 )
		      )
		      (+ (* 1000 (atof (substr (caar y) 2)))
			 (atof
			   (substr (caar y)
				   (+ 2 (vl-string-search "+" (caar y)))
			   )
			 )
		      )
		    )
		  )
	       )
	     )
	   )
    (write-line n file)
  )
  (close file)
  (princ)
)
(defun amllst (lst)
  (if lst
    (cons (mapcar 'cdr
		  (vl-remove-if-not
		    '(lambda (x) (equal (caar lst) (car x)))
		    lst
		  )
	  )
	  (amllst
	    (vl-remove-if '(lambda (x) (equal (caar lst) (car x))) lst)
	  )
    )
    nil
  )
)
(defun arrlst (lst)
  (mapcar
    '(lambda (x)
       (vl-sort
	 (vl-sort x
		  '(lambda (a b) (> (cadr (last a)) (cadr (last b))))
	 )
	 '(lambda (a b) (< (car (last a)) (cadr (last b))))
       )
     )
    (amllst (vl-sort lst '(lambda (a b) (< (car a) (car b)))))
  )
)
(defun cltx (lst)
  (setq	n 0
	m 0
  )
  (append
    (list (caar lst))
    (list (apply 'strcat
	   (mapcar '(lambda (x) (strcat x "    ")) (cdar lst))
    ))
    (mapcar
      '(lambda (x)
	 (apply	'strcat
		(mapcar	'(lambda (d) (strcat d "    "))
			(append (list (strcat "多段线" (itoa (setq n (1+ n))))
			      (strcat "颜色" (itoa (car x))))
			      (apply 'append (mapcar '(lambda (y)
					 (list (strcat "X=" (rtos (car y) 2 4))
					       (strcat "Y=" (rtos (cadr y) 2 4))
					       "z=0.0000"
					 )
				       )
				      (cdr x)
			      ))
			)
		)
	 )
       )
      (cadr lst)
    )
    (mapcar
      '(lambda (x)
	 (apply	'strcat
		(mapcar	'(lambda (d) (strcat d "    "))
			(append (list (strcat "直线" (itoa (setq m (1+ m))))
			      (strcat "颜色" (itoa (car x))))
			      (apply 'append (mapcar '(lambda (y)
					 (list (strcat "X=" (rtos (car y) 2 4))
					       (strcat "Y=" (rtos (cadr y) 2 4))
					       "z=0.0000"
					 )
				       )
				      (cdr x)
			      ))
			)
		)
	 )
       )
      (caddr lst)
    )
  )
)

















	 
(princ "/n——————测试版命令tt——————")