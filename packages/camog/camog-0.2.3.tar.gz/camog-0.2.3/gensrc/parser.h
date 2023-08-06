    if (c == ' ') {
        do {
            
            NEXTCHAR_NOQUOTES(goodend);
        } while (c == ' ');
    }
    else {
    }
    if ((digit = c ^ '0') <= 9) {
        
        NEXTCHAR_NOQUOTES(goodend);
        if ((digit = c ^ '0') <= 9) {
            do {
                
                NEXTCHAR_NOQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9);
        }
        else {
        }
        if (c == '.') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_NOQUOTES(goodend);
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
        if ((c | 32) == 'e') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_NOQUOTES(badend);
            if (c == '+') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else if (c == '-') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_NOQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
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
        NEXTCHAR_NOQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            
            NEXTCHAR_NOQUOTES(goodend);
        }
        else {
            goto bad;
        }
        if ((digit = c ^ '0') <= 9) {
            do {
                
                NEXTCHAR_NOQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9);
        }
        else {
        }
        if ((c | 32) == 'e') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_NOQUOTES(badend);
            if (c == '+') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else if (c == '-') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_NOQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
    }
    else if ((c | 32) == 'i') {
        
        NEXTCHAR_NOQUOTES(badend);
        if ((c | 32) == 'n') {
            
            NEXTCHAR_NOQUOTES(badend);
        }
        else {
            goto bad;
        }
        if ((c | 32) == 'f') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_NOQUOTES(goodend);
        }
        else {
            goto bad;
        }
    }
    else if ((c | 32) == 'n') {
        
        NEXTCHAR_NOQUOTES(badend);
        if ((c | 32) == 'a') {
            
            NEXTCHAR_NOQUOTES(badend);
        }
        else {
            goto bad;
        }
        if ((c | 32) == 'n') {
            if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
            NEXTCHAR_NOQUOTES(goodend);
        }
        else {
            goto bad;
        }
    }
    else if (c == '+') {
        
        NEXTCHAR_NOQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            
            NEXTCHAR_NOQUOTES(goodend);
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if (c == '.') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(goodend);
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_NOQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_NOQUOTES(goodend);
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
            NEXTCHAR_NOQUOTES(badend);
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_NOQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_NOQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if ((c | 32) == 'i') {
            
            NEXTCHAR_NOQUOTES(badend);
            if ((c | 32) == 'n') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'f') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else if ((c | 32) == 'n') {
            
            NEXTCHAR_NOQUOTES(badend);
            if ((c | 32) == 'a') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'n') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(goodend);
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
        
        NEXTCHAR_NOQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            
            NEXTCHAR_NOQUOTES(goodend);
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if (c == '.') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(goodend);
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_NOQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_NOQUOTES(goodend);
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
            NEXTCHAR_NOQUOTES(badend);
            if ((digit = c ^ '0') <= 9) {
                
                NEXTCHAR_NOQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if ((c | 32) == 'e') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else if (c == '-') {
                    
                    NEXTCHAR_NOQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    
                    NEXTCHAR_NOQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR_NOQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if ((c | 32) == 'i') {
            
            NEXTCHAR_NOQUOTES(badend);
            if ((c | 32) == 'n') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'f') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else if ((c | 32) == 'n') {
            
            NEXTCHAR_NOQUOTES(badend);
            if ((c | 32) == 'a') {
                
                NEXTCHAR_NOQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'n') {
                if (col_type == COL_TYPE_INT64) { columns[col_idx].type = col_type = COL_TYPE_DOUBLE; }
                NEXTCHAR_NOQUOTES(goodend);
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
            
            NEXTCHAR_NOQUOTES(goodend);
        } while (c == ' ');
    }
    else {
    }
