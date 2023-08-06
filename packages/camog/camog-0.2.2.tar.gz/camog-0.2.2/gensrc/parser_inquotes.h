    if (c == ' ') {
        do {
            
            NEXTCHAR_INQUOTES(goodend);
        } while (c == ' ');
    }
    else {
    }
    if ((digit = c ^ '0') <= 9) {
        
        NEXTCHAR_INQUOTES(goodend);
        if ((digit = c ^ '0') <= 9) {
            do {
                
                NEXTCHAR_INQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9);
        }
        else {
        }
        if (c == '.') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(goodend);
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
        if ((c | 32) == 'e') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(badend);
            if (c == '+') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else if (c == '-') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
    }
    else if (c == '.') {
        if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
        NEXTCHAR_INQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            
            NEXTCHAR_INQUOTES(goodend);
        }
        else {
            goto bad;
        }
        if ((digit = c ^ '0') <= 9) {
            do {
                
                NEXTCHAR_INQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9);
        }
        else {
        }
        if ((c | 32) == 'e') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(badend);
            if (c == '+') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else if (c == '-') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
    }
    else if ((c | 32) == 'i') {
        
        NEXTCHAR_INQUOTES(badend);
        if ((c | 32) == 'n') {
            
            NEXTCHAR_INQUOTES(badend);
        }
        else {
            goto bad;
        }
        if ((c | 32) == 'f') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(goodend);
        }
        else {
            goto bad;
        }
    }
    else if ((c | 32) == 'n') {
        
        NEXTCHAR_INQUOTES(badend);
        if ((c | 32) == 'a') {
            
            NEXTCHAR_INQUOTES(badend);
        }
        else {
            goto bad;
        }
        if ((c | 32) == 'n') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(goodend);
        }
        else {
            goto bad;
        }
    }
    else if (c == '+') {
        
        NEXTCHAR_INQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            
            NEXTCHAR_INQUOTES(goodend);
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if (c == '.') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(goodend);
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if (c == '.') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(badend);
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if ((c | 32) == 'i') {
            
            NEXTCHAR_INQUOTES(badend);
            if ((c | 32) == 'n') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'f') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else if ((c | 32) == 'n') {
            
            NEXTCHAR_INQUOTES(badend);
            if ((c | 32) == 'a') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'n') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else {
            goto bad;
        }
    }
    else if (c == '-') {
        
        NEXTCHAR_INQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            
            NEXTCHAR_INQUOTES(goodend);
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if (c == '.') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(goodend);
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if (c == '.') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_INQUOTES(badend);
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if ((c | 32) == 'i') {
            
            NEXTCHAR_INQUOTES(badend);
            if ((c | 32) == 'n') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'f') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else if ((c | 32) == 'n') {
            
            NEXTCHAR_INQUOTES(badend);
            if ((c | 32) == 'a') {
                
                NEXTCHAR_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'n') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else {
            goto bad;
        }
    }
    else {
    }
    if (c == ' ') {
        do {
            
            NEXTCHAR_INQUOTES(goodend);
        } while (c == ' ');
    }
    else {
    }
