                                                                                       
           import os                                                                                                                  
           from multiprocess import Process                                                                                           
                                                                                                                                      
           def print_hello_world():                                                                                                   
               """Função para imprimir "Hello, World!""""                                                                             
                                                                                                                                      
               # Imprimindo mensagem no console.                                                                                      
               message = ' Hello from process: {}'.format(os.getpid())                                                                
                                                                                                                                      
               for _ in range(3):                                                                                                     
                   time.sleep(.5)                                                                                                     
                                                                                                                                      
                  if os.name == 'posix':                                                                                              
                       print('\n{}\                                                     